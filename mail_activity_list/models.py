# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class ActivityWithRecordReference(models.Model):
    """Add the record reference field."""

    _inherit = 'mail.activity'

    record_reference = fields.Char(compute='_compute_record_reference', store=True)

    @api.depends('res_model_id', 'res_id')
    def _compute_record_reference(self):
        for activity in self:
            activity.record_reference = ','.join([activity.res_model, str(activity.res_id)])


class ActivityWithEffectiveDate(models.Model):
    """Add the effective date field."""

    _inherit = 'mail.activity'

    effective_date = fields.Date(compute='_compute_effective_date', store=True)

    @api.depends('date_done', 'date_deadline')
    def _compute_effective_date(self):
        for activity in self:
            activity.effective_date = activity.date_done or activity.date_deadline


class ActivityWithoutFalseInDisplayName(models.Model):
    """Prevent an activity with the display name False."""

    _inherit = 'mail.activity'

    effective_date = fields.Date(compute='_compute_effective_date', store=True)

    @api.multi
    def name_get(self):
        default_name = _('Activity')
        return [(a.id, a.summary or default_name) for a in self]
