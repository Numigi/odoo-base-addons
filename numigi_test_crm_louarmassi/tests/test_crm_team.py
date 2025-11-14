# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date, timedelta

from odoo.tests.common import tagged, users
from odoo.tests.common import Form
from odoo.addons.crm.tests.common import TestCrmCommon

class TestCrmTeam(TestCrmCommon):

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
    
