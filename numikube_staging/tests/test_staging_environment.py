# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo.tests.common import TransactionCase


class TestStagingEnvironment(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = "http://lab.example.com"
        cls.environment = cls.env["staging.environment"].create(
            {
                "name": "Lab",
                "url": cls.url,
            }
        )

    def test_database_selector_url(self):
        assert self.environment.database_selector_url == (
            f"{self.url}/web/database/selector"
        )
