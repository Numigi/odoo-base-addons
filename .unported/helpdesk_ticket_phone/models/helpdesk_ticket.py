# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _name = "helpdesk.ticket"
    _inherit = ["helpdesk.ticket", "phone.validation.mixin"]

    partner_phone = fields.Char()
    partner_mobile = fields.Char()

    @api.onchange('partner_id')
    def _onchange_partner_set_phone(self):
        if self.partner_id:
            self.partner_phone = self.partner_id.phone
            self.partner_mobile = self.partner_id.mobile

    
    def _set_phone_number_format(self):
        for record in self.with_context(skip_set_phone_format=True):
            phone = self.phone_format(
                record.partner_phone or "",
                country=record.partner_id.country_id,
                company=record.company_id
            )
            mobile = self.phone_format(
                record.partner_mobile or "",
                country=record.partner_id.country_id,
                company=record.company_id
            )

            if record.partner_phone != phone:
                record.partner_phone = phone

            if record.partner_mobile != mobile:
                record.partner_mobile = mobile

    @api.model
    def create(self, vals):
        res = super().create(vals)

        if not res.partner_phone:
            res.partner_phone = res.partner_id.phone

        if not res.partner_mobile:
            res.partner_mobile = res.partner_id.mobile

        res._set_phone_number_format()
        return res

    
    def write(self, vals):
        res = super().write(vals)
        if not self._context.get("skip_set_phone_format"):
            self._set_phone_number_format()
        return res
