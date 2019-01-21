# © 2015 ABF OSIELL <https://osiell.com>
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from typing import Iterable, Mapping
from odoo import models, fields, api, modules, tools, _

FIELDS_BLACKLIST = {
    'id', 'create_uid', 'create_date', 'write_uid', 'write_date',
    'display_name', '__last_update', 'password',
}


class AuditlogRule(models.Model):
    _name = 'auditlog.rule'
    _description = "Auditlog - Rule"

    name = fields.Char("Name", required=True)
    model_id = fields.Many2one(
        'ir.model', "Model", required=True,
        help="Select model for which you want to generate log.")
    log_write = fields.Boolean(
        "Log Writes", default=True,
        help=("Select this if you want to keep track of modification on any "
              "record of the model of this rule"))
    log_unlink = fields.Boolean(
        "Log Deletes", default=True,
        help=("Select this if you want to keep track of deletion on any "
              "record of the model of this rule"))
    log_create = fields.Boolean(
        "Log Creates", default=True,
        help=("Select this if you want to keep track of creation on any "
              "record of the model of this rule"))
    state = fields.Selection(
        [('draft', "Draft"), ('subscribed', "Subscribed")],
        string="State", required=True, default='draft')
    action_id = fields.Many2one('ir.actions.act_window', string="Action")

    _sql_constraints = [
        ('model_uniq', 'unique(model_id)',
         ("There is already a rule defined on this model\n"
          "You cannot define another: please edit the existing one."))
    ]

    @api.model
    def create(self, vals):
        """Update the registry when a new rule is created."""
        new_record = super().create(vals)
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return new_record

    @api.multi
    def write(self, vals):
        """Update the registry when existing rules are updated."""
        super().write(vals)
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return True

    @api.multi
    def unlink(self):
        """Unsubscribe rules before removing them."""
        super().unlink()
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return True

    @api.multi
    def subscribe(self):
        for rule in self:
            rule.state = 'subscribed'
            if not rule.action_id:
                rule.action_id = rule._create_auditlog_shortcut()
        return True

    def _create_auditlog_shortcut(self):
        """Create a shortcut to view the logs of a record form the form view."""
        shortcut = self.env['ir.actions.act_window'].sudo().create({
            'name': "Logs",
            'res_model': 'auditlog.log.line',
            'src_model': self.model_id.model,
            'binding_model_id': self.model_id.id,
            'domain': (
                "[('log_id.model_id', '=', {model_id}), ('log_id.res_id', '=', active_id)]"
                .format(model_id=self.model_id.id)
            ),
            'context': "{'field_logs_from_record_form': True}",
            'groups_id': [(4, self.env.ref('auditlog.group_view_audit_logs').id)],
        })

        for lang in self.env['res.lang'].search([]):
            shortcut.with_context(lang=lang.code).name = (
                self.with_context(lang=lang.code)._get_shortcut_label())

        return shortcut

    @api.model
    def _get_shortcut_label(self):
        """Get the label for the `Action` button on the form view of a record.

        This must be isolated in a seperate method so that the label is translated
        in a specific language.
        """
        return _('Logs')

    @api.multi
    def unsubscribe(self):
        # Remove the shortcut to view logs
        self.mapped('action_id').unlink()
        self.write({'state': 'draft'})
        modules.registry.Registry(self.env.cr.dbname).clear_caches()
        return True


class BaseWithAuditLogs(models.AbstractModel):

    _inherit = 'base'

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals, **kwargs):
        if not self._is_auditlog_enabled('create'):
            return super().create(vals, **kwargs)

        fields_to_log = list(vals.keys())
        new_record = super().create(vals, **kwargs)
        values = new_record._get_auditlog_field_values(fields_to_log)
        OperationLogger(new_record, 'create').log_operation(fields_to_log, {}, values)
        return new_record

    @api.multi
    def write(self, vals, **kwargs):
        if not self._is_auditlog_enabled('write'):
            return super().write(vals, **kwargs)

        fields_to_log = list(vals.keys())
        values_before = self._get_auditlog_field_values(fields_to_log)
        super().write(vals, **kwargs)
        values_after = self._get_auditlog_field_values(fields_to_log)
        OperationLogger(self, 'write').log_operation(fields_to_log, values_before, values_after)
        return True

    @api.multi
    def unlink(self, **kwargs):
        if self._is_auditlog_enabled('unlink'):
            OperationLogger(self, 'unlink').log_operation({}, {}, {})

        return super().unlink(**kwargs)

    @tools.ormcache('operation')
    def _is_auditlog_enabled(self, operation):
        """Check if the operation is logged for the given model."""
        log_field = 'log_{operation}'.format(operation=operation)
        count = self.env['auditlog.rule'].sudo().search([
            ('model_id.model', '=', self._name),
            (log_field, '=', True),
            ('state', '=', 'subscribed')
        ], count=True)
        return count > 0

    def _get_auditlog_field_values(self, field_names):
        """Get the values of the given fields for the given records.

        :param records: a recordset
        :param field_names: the names of the fields to read.
        """
        return dict(
            (d['id'], d) for d in self.sudo()
            .with_context(prefetch_fields=False).read(list(field_names))
        )


class OperationLogger:
    """Class responsible for logging an operation on an Odoo recordset."""

    def __init__(self, records, method):
        """Initialize the operation logger.

        :param records: the records to log.
        :param method: the method to log.
        """
        self._user = records.env.user
        self._records = records.sudo()
        self._method = method
        self._env = records.env
        self._model = records._name
        self._model_record = self._env['ir.model'].sudo()._get(self._model)
        self._field_records = {f.name: f for f in self._model_record.field_id}
        self._http_request = self._env['auditlog.http.request'].sudo().current_http_request()

    def log_operation(
        self,
        fields_updated: Iterable[str],
        old_values: Mapping[int, dict],
        new_values: Mapping[int, dict],
    ):
        for record in self._records.sudo():
            self._log_operation_for_single_record(record, fields_updated, old_values, new_values)

    def _log_operation_for_single_record(
        self,
        record,
        fields_updated: Iterable[str],
        old_values: Mapping[int, dict],
        new_values: Mapping[int, dict],
    ):
        """Create a log entry for the given record.

        :param record: the record for which to log the operation
        :param fields_updated: the fields updated during the operation
        :param old_values: the field values before the operation
        :param new_values: the values after the operation
        """
        log = self._env['auditlog.log'].sudo().create({
            'name': record.display_name,
            'model_id': self._model_record.id,
            'res_id': record.id,
            'method': self._method,
            'user_id': self._user.id,
            'http_request_id': self._http_request.id,
        })

        if fields_updated:
            record_old_values = old_values.get(record.id) or {}
            record_new_values = new_values.get(record.id) or {}

            self._create_log_lines(log, fields_updated, record_old_values, record_new_values)

    def _create_log_lines(
        self,
        log,
        fields_updated: Iterable[str],
        old_values: dict,
        new_values: dict,
    ):
        """Create a log line for each updated field.

        :param log: the parent `auditlog.log` record.
        :param old_value: the values before the operation.
        :param new_values: the values after the operation.
        """
        fields_to_log = {
            self._field_records.get(f) for f in fields_updated
            if f not in FIELDS_BLACKLIST and f in self._field_records
        }

        for field in fields_to_log:
            value_before = old_values.get(field.name)
            value_after = new_values.get(field.name)
            self._env['auditlog.log.line'].sudo().create({
                'field_id': field.id,
                'log_id': log.id,
                'old_value': self._format_field_value(field, value_before),
                'new_value': self._format_field_value(field, value_after),
            })

    def _format_field_value(self, field, value):
        """Format a field value.

        :param field: the ir.model.fields record for which to format the value
        :param value: the value to format
        :return: the formated value
        """
        if value is None:
            return value

        is_x2many_field = field.relation and '2many' in field.ttype
        if is_x2many_field:
            return self._format_x2many_field_value(field, value)
        else:
            return value

    def _format_x2many_field_value(self, field, value):
        """Format the value of an x2many field.

        :param field: the ir.model.fields record for which to format the value
        :param value: the value to format
        :return: the formated value
        """
        related_model_cls = self._env[field.relation]

        # Filter IDs to prevent a 'name_get()' call on deleted resources
        existing_records = related_model_cls.browse(value).exists()

        value_text = []
        value_text.extend(existing_records.name_get())

        # Deleted resources will have a 'DELETED' text representation
        deleted_ids = set(value) - set(existing_records.ids)
        value_text.extend(((i, 'DELETED') for i in deleted_ids))

        return value_text
