# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tests.common import SavepointCase


class TestHelpdeskTicket(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.partner = cls.env["res.partner"].create(
            {"name": "william", "email": "william@gmail.com"}
        )

        cls.ticket = cls.env["helpdesk.ticket"].create(
            {
                "name": "test",
                "description": "test",
                "partner_id": cls.partner.id,
            }
        )

    def test_no_mail(self):
        assert not self.ticket.message_ids.filtered(lambda m: "Thank you," in m.body)
