# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from _datetime import timedelta
from werkzeug.urls import url_join


class Lead(models.Model):
    _inherit = "crm.lead"

    expected_revenue = fields.Monetary(groups="sales_team.group_sale_manager")

    @api.model
    def _notify_members(self):
        template = self.env.ref(
            "numigi_test_crm_louarmassi.email_template_notify_members", raise_if_not_found=False
        )
        new_leads = self._get_draft_leads_10days()
        for lead in new_leads:
            template.send_mail(lead.id, force_send=True)

    @api.model
    def _get_draft_leads_10days(self):
        stage_new = self.env.ref("crm.stage_lead1")
        date_before_10days = fields.Datetime.now() - timedelta(days=10)
        lead_domain = [
            ("type", "=", "opportunity"),
            ("stage_id", "=", stage_new.id),
            ("date_last_stage_update", "<=", date_before_10days),
            ("team_id", "!=", False),
        ]
        new_leads = self.search(lead_domain)
        return new_leads

    def get_access_link(self):
        self.ensure_one()
        web_base_url = self.get_base_url()
        access_link = url_join(web_base_url, f"/web#id={self.id}&model=crm.lead&view_type=form")
        return access_link
