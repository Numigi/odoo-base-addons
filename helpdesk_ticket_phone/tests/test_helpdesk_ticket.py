# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models
from odoo.tests import common


class TestHelpdeskTicket(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({
            "name": "Some Partner",
            "country_id": cls.env.ref("base.ca").id,
            "phone": "5144445555",
            "mobile": "4184445555",
        })
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {"name": "/", "description": "/", "partner_id": cls.partner.id}
        )

    def test_create(self):
        assert self.ticket.partner_phone == "+1 514-444-5555"
        assert self.ticket.partner_mobile == "+1 418-444-5555"

    def test_write_partner_phone(self):
        self.ticket.partner_phone = "5146667777"
        self.ticket.refresh()
        assert self.ticket.partner_phone == "+1 514-666-7777"

    def test_write_partner_mobile(self):
        self.ticket.partner_mobile = "5146667777"
        self.ticket.refresh()
        assert self.ticket.partner_mobile == "+1 514-666-7777"

    def test_onchange_partner(self):
        ticket = self.env["helpdesk.ticket"].new({})
        ticket.partner_id = self.partner
        ticket._onchange_partner_set_phone()
        assert ticket.partner_phone == self.partner.phone
        assert ticket.partner_mobile == self.partner.mobile
