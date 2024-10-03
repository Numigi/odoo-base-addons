# Copyright 2024  Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestPermission(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group_user = cls.env.ref("base.group_user")
        cls.group_admin_filter = cls.env.ref("admin_light_filters.group_custom_filters")
        cls.user_1 = cls._create_user(
            "user_1", [cls.group_user, cls.group_admin_filter]
        )
        cls.user_2 = cls._create_user("user_2", [cls.group_user])

    @classmethod
    def _create_user(cls, login, groups):
        group_ids = [group.id for group in groups]
        user = cls.env["res.users"].create(
            {
                "name": "Test User",
                "login": login,
                "password": "Demo_12345",
                "email": "%s@yourcompany.com" % login,
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user

    def test_05_delete_filter(self):
        test_filter = self.env["ir.filters"].create(
            {
                "name": "Test filter",
                "model_id": "ir.filters",
                "user_id": False,
                "manual_user_ids": [(6, 0, (self.user_1 + self.user_2).ids)],
            }
        )
        test_filter.with_user(self.user_1).unlink()
