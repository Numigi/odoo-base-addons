# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _inherit = ["helpdesk.ticket", "phone.validation.mixin"]

    partner_phone = fields.Char()
    partner_mobile = fields.Char()

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super(HelpdeskTicket, self)._onchange_partner_id()
        if self.partner_id:
            self.partner_phone = self.partner_id.phone
            self.partner_mobile = self.partner_id.mobile

    @api.multi
    def _set_phone_number_format(self):
        for record in self:
            if record.partner_phone:
                record.with_context(skip_set_phone_format=True).write(
                    {
                        'partner_phone':
                            self.phone_format(
                                record.partner_phone,
                                country=record.partner_id.country_id,
                                company=record.company_id
                            )
                    }
                )
            if record.partner_mobile:
                record.with_context(skip_set_phone_format=True).write(
                    {
                        'partner_mobile':
                            self.phone_format(
                                record.partner_mobile,
                                country=record.partner_id.country_id,
                                company=record.company_id
                            )
                    }
                )

    @api.model
    def create(self, vals):
        res = super(HelpdeskTicket, self).create(vals)
        res._set_phone_number_format()
        return res

    @api.multi
    def write(self, vals):
        res = super(HelpdeskTicket, self).write(vals)
        if not self._context.get("skip_set_phone_format"):
            self._set_phone_number_format()
        return res
