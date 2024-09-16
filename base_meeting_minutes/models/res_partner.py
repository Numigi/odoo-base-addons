# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    meeting_minutes_count = fields.Integer(
        string="Meeting Minutes",
        compute="_compute_meeting_minutes_count",
    )

    @api.multi
    def _compute_meeting_minutes_count(self):
        for record in self:
            domain = [("partner_ids", "in", record.id)]
            record.meeting_minutes_count = len(
                self.env["meeting.minutes.mixin"].search(domain)
            )

    def action_show_meeting_minutes(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Meeting Minutes"),
            "res_model": "meeting.minutes.mixin",
            "domain": [
                ("partner_ids", "in", self.id),
            ],
            "view_mode": "tree,form",
        }
