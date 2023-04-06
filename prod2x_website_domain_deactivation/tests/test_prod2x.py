# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestProd2x(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.initial_domain = "test.com"
        cls.company = cls.env["res.company"].create(
            {
                "name": "test",
            }
        )
        cls.lang = cls.env["res.lang"].create(
            {
                "name": "test",
                "code": "test",
            }
        )
        cls.website = cls.env["website"].create(
            {
                "name": "test",
                "company_id": cls.company.id,
                "default_lang_id": cls.lang.id,
                "domain": cls.initial_domain,
            }
        )

    def test_email_marketing_disabled(self):
        self.env["prod2x"].run()
        assert not self.website.domain
