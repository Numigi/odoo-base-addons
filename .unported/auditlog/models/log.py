# © 2015 ABF OSIELL <https://osiell.com>
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models, fields

LIST_DISPLAYED_VALUES_MAX_LENGTH = 60


class AuditlogLog(models.Model):

    _name = 'auditlog.log'
    _description = "Auditlog - Log"
    _order = "create_date desc"

    name = fields.Char("Resource Name")
    model_id = fields.Many2one('ir.model', string="Model")
    res_id = fields.Integer("Resource ID")
    user_id = fields.Many2one('res.users', string="User")
    method = fields.Selection([
        ('write', 'Write'),
        ('create', 'Create'),
        ('unlink', 'Delete'),
    ], "Operation")
    line_ids = fields.One2many('auditlog.log.line', 'log_id', string="Fields updated")
    http_request_id = fields.Many2one('auditlog.http.request', string="HTTP Request")


class AuditlogLogLine(models.Model):

    _name = 'auditlog.log.line'
    _description = "Auditlog - Log details (fields updated)"
    _order = "create_date desc"

    field_id = fields.Many2one('ir.model.fields', ondelete='cascade', string="Field", required=True)
    log_id = fields.Many2one('auditlog.log', string="Log", ondelete='cascade', index=True)
    old_value = fields.Text("Old Value")
    new_value = fields.Text("New Value")
    field_name = fields.Char("Technical name", related='field_id.name')
    field_description = fields.Char("Description", related='field_id.field_description')

    name = fields.Char(related='log_id.name')
    model_id = fields.Many2one(related='log_id.model_id', store=True)
    res_id = fields.Integer(related='log_id.res_id', store=True)
    user_id = fields.Many2one(related='log_id.user_id', store=True)
    method = fields.Selection(related='log_id.method')
    http_request_id = fields.Many2one(related='log_id.http_request_id')


class AuditLogLineWithLimitedValueText(models.Model):

    _inherit = 'auditlog.log.line'

    old_value_display = fields.Char(compute='_compute_displayed_values')
    new_value_display = fields.Char(compute='_compute_displayed_values')

    def _compute_displayed_values(self):
        for line in self:
            line.old_value_display = (line.old_value or '')[:LIST_DISPLAYED_VALUES_MAX_LENGTH]
            line.new_value_display = (line.new_value or '')[:LIST_DISPLAYED_VALUES_MAX_LENGTH]
