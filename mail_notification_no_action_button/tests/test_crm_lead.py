# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data
from odoo.tests import SavepointCase


@ddt
class TestCRMLead(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].create({
            'name': 'test@example.com',
            'email': 'test@example.com',
            'login': 'test@example.com',
        })
        cls.partner = cls.user.partner_id
        cls.lead = cls.env['crm.lead'].create({
            'name': 'M Lead',
        })
        cls.lead.message_subscribe([cls.partner.id])

    def send_notification_email(self):
        message = self.lead.message_post(body='Test')
        message._notify(self.lead, {'partner_ids': [(4, self.partner.id)]}, mail_auto_delete=False)
        return self.env['mail.mail'].search([('mail_message_id', '=', message.id)], limit=1)

    @data('Won', 'Lost', 'Sales Team Settings')
    def test_action_buttons_removed(self, button_label):
        email = self.send_notification_email()
        assert button_label not in email.body_html
