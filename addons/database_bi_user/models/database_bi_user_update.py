# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from itertools import groupby
from odoo import api, models, tools
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


def _logged_query(cr, query, args=()):
    _logger.info(query % args)
    cr.execute(query, args)


class DatabaseBIUserUpdate(models.TransientModel):

    _name = 'database.bi.user.update'
    _description = 'Update the BI Database User'

    def _create_role_if_not_exists(self):
        _logged_query(self._cr, "SELECT 1 FROM pg_roles WHERE rolname='bi'")
        role_exists = bool(self._cr.fetchone())

        if role_exists:
            _logger.info('The bi database role already exists')
        else:
            _logger.info('Creating the bi database role')
            _logged_query(self._cr, "CREATE ROLE bi")

    def _allow_login(self):
        _logged_query(self._cr, "ALTER ROLE bi WITH LOGIN")

    def _grant_select_on_all_tables(self):
        _logged_query(self._cr, "GRANT SELECT ON ALL TABLES IN SCHEMA public TO bi")

    @api.model
    def setup_role(self):
        if not self.env.user._is_admin():
            raise AccessError('You are not allowed to update the BI user.')

        self._create_role_if_not_exists()
        self._allow_login()
        self._grant_select_on_all_tables()

    @api.model
    def set_password(self, password):
        if not self.env.user._is_admin():
            raise AccessError('You are not allowed to change the BI user password.')

        _logger.info('Updating database bi user password')
        _logged_query(self._cr, 'ALTER ROLE bi WITH ENCRYPTED PASSWORD %s', (password, ))


def _is_stored_column_field(env: api.Environment, field: 'ir.model.fields'):
    model = env.get(field.model)
    return model is not None and tools.column_exists(env.cr, model._table, field.name)


def _get_field_table_name(env: api.Environment, field: 'ir.model.fields'):
    model = env.get(field.model)
    return model._table


class DatabaseBIUserUpdateWithPrivateColumns(models.TransientModel):
    """Prevent the BI user from accessing columns of private fields.

    Private fields are defined in the module private_data_group.
    https://github.com/Numigi/odoo-base-addons/tree/12.0/private_data_group

    The strategy is to REVOKE access on a table that contains any private column.
    Then, GRANT access to each non-private column on this table.

    This complexity is required because a GRANT on a table takes precedence
    over a specific column REVOKE.

    See detailed explanation here:
    https://www.postgresql.org/message-id/20060130044430.GA42463@rufus.net
    """

    _inherit = 'database.bi.user.update'

    def _revoke_select_on_table(self, table_name):
        _logged_query(
            self._cr,
            "REVOKE SELECT ON TABLE {table} FROM bi".format(table=table_name)
        )

    def _grant_select_on_columns(self, table_name, columns):
        _logged_query(
            self._cr,
            "GRANT SELECT ({columns}) ON TABLE {table} TO bi".format(
                table=table_name,
                columns=','.join(columns),
            )
        )

    def _revoke_select_on_private_columns(self):
        private_fields = self.env['ir.private.field'].search([])
        private_columns = (
            f.field_id for f in private_fields if _is_stored_column_field(self.env, f.field_id)
        )
        grouped_private_columns = groupby(
            private_columns, lambda c: _get_field_table_name(self.env, c)
        )

        for table_name, group in grouped_private_columns:
            self._revoke_select_on_table(table_name)

            all_table_columns = set(tools.table_columns(self._cr, table_name))
            private_column_names = {c.name for c in group}
            non_private_columns = all_table_columns.difference(private_column_names)

            if non_private_columns:
                self._grant_select_on_columns(table_name, non_private_columns)

    @api.model
    def setup_role(self):
        super().setup_role()
        self._revoke_select_on_private_columns()
