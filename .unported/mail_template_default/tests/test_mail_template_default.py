# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestMailTemplateDefault(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mail_1 = cls.env["mail.template"].create({
            "name": "Mail to Partner 1",
            "model_id": cls.env.ref("base.model_res_partner").id,
        })
        cls.mail_2 = cls.env["mail.template"].create({
            "name": "Mail to Partner 2",
            "model_id": cls.env.ref("base.model_res_partner").id,
        })

    def test_model_can_have_one_template(self):
        self.mail_1.is_default_template = True

    def test_model_cannot_have_many_template(self):
        self.mail_1.is_default_template = True
        with self.assertRaises(ValidationError):
            self.mail_2.is_default_template = True

    def test_get_default_template(self):
        self.mail_1.is_default_template = True
        self.assertEquals(
            self.env["mail.compose.message"].with_context(
                default_model="res.partner"
            ).default_get(["template_id"])["template_id"],
            self.mail_1.id
        )
        self.mail_1.is_default_template = False
        self.assertEquals(
            self.env["mail.compose.message"].with_context(default_model="res.partner").default_get(["template_id"]),
            {}
        )
