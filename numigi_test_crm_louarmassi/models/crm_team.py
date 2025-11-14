# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class Team(models.Model):
    _inherit = "crm.team"

    emails = fields.Char("Emails", compute="_compute_emails")

    @api.depends("member_ids.email")
    def _compute_emails(self):
        for team in self:
            members_email = [member.email for member in team.member_ids if member.email]
            team.emails = ",".join(members_email)

    @api.onchange('user_id')
    def onchange_user_id(self):
        if self.user_id:
            self.member_ids = [(4, self.user_id.id)]
    