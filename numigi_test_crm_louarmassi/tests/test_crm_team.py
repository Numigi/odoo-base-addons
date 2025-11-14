# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date, timedelta
from odoo import fields
from odoo.tests.common import tagged, users
from odoo.tests.common import Form
from odoo.addons.crm.tests.common import TestCrmCommon


class TestCrmTeam(TestCrmCommon):
    @classmethod
    def setUpClass(cls):
        super(TestCrmTeam, cls).setUpClass()
        cls.opport_1 = cls.env["crm.lead"].create(
            {
                "name": "Nibbler Spacecraft Request",
                "type": "opportunity",
                "user_id": cls.user_sales_leads.id,
                "team_id": cls.sales_team_1.id,
                "partner_id": False,
                "contact_name": "Amy Wong",
                "email_from": "amy.wong@test.example.com",
                "country_id": cls.env.ref("base.us").id,
                "stage_id": cls.env.ref("crm.stage_lead1").id,
            }
        )

    def test_crm_team_emails(self):
        """Test Emails field containing all email addresses of team members,
        separated by commas."""
        field_emails = self.sales_team_1.emails.split(",")
        member_emails = [member.email for member in self.sales_team_1.member_ids if member.email]
        self.assertEqual(field_emails, member_emails)

    def test_crm_team_manager(self):
        """Test if a team manager is also a team member"""
        team_form = Form(self.sales_team_1)
        team_form.user_id = self.user_sales_manager
        self.assertIn(team_form.user_id, team_form.member_ids)

    def test_draft_leads_10days(self):
        self.opport_1.write(
            {
                "date_last_stage_update": fields.Datetime.now() - timedelta(days=11),
            }
        )
        draft_before_10days_leads = self.env["crm.lead"]._get_draft_leads_10days()
        self.assertIn(self.opport_1, draft_before_10days_leads)
        self.opport_1.write(
            {
                "date_last_stage_update": fields.Datetime.now() - timedelta(days=9),
            }
        )
        draft_before_10days_leads = self.env["crm.lead"]._get_draft_leads_10days()
        self.assertNotIn(self.opport_1, draft_before_10days_leads)
