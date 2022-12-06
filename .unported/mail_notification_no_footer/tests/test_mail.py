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
        cls.subtype = cls.env.ref("mail.mt_comment")
        cls.lead.message_subscribe([cls.partner.id], subtype_ids=[cls.subtype.id])

    def send_notification_email(self):
        message = self.lead.message_post(
            body="Test", mail_auto_delete=False, send_after_commit=False, force_send=True,
            subtype_id=self.subtype.id,
        )
        return self.env["mail.mail"].search(
            [("mail_message_id", "=", message.id)], limit=1
        )

    @data(
        "odoo.com",
        "Sent",
        "using",
    )
    def test_notification_has_term(self, term):
        email = self.send_notification_email()
        assert term not in email.body_html
