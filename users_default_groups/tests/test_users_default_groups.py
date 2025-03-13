# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestDefaultUserRights(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.default_user = cls.env.ref("base.default_user")
        cls.group = cls.env.ref("base.group_user")
        cls.default_user.write({"groups_id": [(4, cls.group.id)]})

    def test_default_user_rights_checked(self):
        self.env["ir.config_parameter"].set_param(
            "base_setup.default_user_rights", True
        )
        self.user = self.env["res.users"].create(
            {
                "name": "Numigi User",
                "login": "numigiuser",
                "email": "numigiuser@example.com",
            }
        )
        # Verify the user has the group like the default user
        self.assertIn(self.group, self.user.groups_id)

    def test_default_user_rights_unchecked(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "base_setup.default_user_rights", False
        )
        self.user = self.env["res.users"].create(
            {
                "name": "Numigi User",
                "login": "numigiuser",
                "email": "numigiuser@example.com",
            }
        )
        # Verify the user doesn't have the group
        not self.assertNotIn(self.group, self.user.groups_id)
