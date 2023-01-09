# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestBotAnwsers(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bot_partner = cls.env.ref("base.partner_root")
        cls.channel = cls.env["mail.channel"].search([], limit=1)

    def test_no_pong(self):
        answer = self._get_answer()
        assert not answer

    def _get_answer(self):
        values = {
            "partner_ids": [(4, self.bot_partner.id)],
        }
        return self.env["mail.bot"]._get_answer(self.channel, "", values, "")
