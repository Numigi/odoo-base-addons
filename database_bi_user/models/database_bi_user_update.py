# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import api, models
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class DatabaseBIUserUpdate(models.TransientModel):

    _name = 'database.bi.user.update'
    _description = 'Update the BI Database User'

    def _create_role_if_not_exists(self):
        self._cr.execute("SELECT 1 FROM pg_roles WHERE rolname='bi'")
        role_exists = bool(self._cr.fetchone())

        if role_exists:
            _logger.info('The bi database role already exists')
        else:
            _logger.info('Creating the bi database role')
            self._cr.execute("CREATE ROLE bi")

    def _allow_login(self):
        self._cr.execute("ALTER ROLE bi WITH LOGIN")

    def _grant_select_on_all_tables(self):
        self._cr.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO bi")

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
        self.env.cr.execute('ALTER ROLE bi WITH ENCRYPTED PASSWORD %s', (password, ))
