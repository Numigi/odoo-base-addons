# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProd2x(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.initial_email = "testing@gmail.com"
        cls.contact = cls.env["mailing.contact"].create(
            {
                "email": cls.initial_email,
            }
        )

    def test_email_marketing_disabled(self):
        self.env["prod2x"].run()
        self.contact.refresh()
        assert self.contact.email != self.initial_email
