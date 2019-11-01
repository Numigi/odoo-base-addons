# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data
from odoo.tests import SavepointCase


@ddt
class TestColorizedBody(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].create({
            'name': 'test@example.com',
            'email': 'test@example.com',
            'login': 'test@example.com',
        })
        cls.partner = cls.user.partner_id
        cls.lead = cls.env['res.partner'].create({
            'name': 'M Lead',
        })
        cls.lead.message_subscribe([cls.partner.id])

    def send_notification_email(self):
        """Send a notification email.

        :return: the email sent
        """
        message = self.lead.message_post(body='Test')
        message._notify(self.lead, {'partner_ids': [(4, self.partner.id)]}, mail_auto_delete=False)
        return self.env['mail.mail'].search([('mail_message_id', '=', message.id)], limit=1)

    @data(
        "odoo.com",
        "Sent",
        "using",
    )
    def test_notification_has_term(self, term):
        email = self.send_notification_email()
        assert term not in email.body_html
