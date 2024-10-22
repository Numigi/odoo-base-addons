# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data

import pytest

from odoo.tests.common import SavepointCase
from odoo.exceptions import AccessError


ADMIN_GROUPS = [
    "base.group_erp_manager",
    "base.group_system",
    "admin_light_base.group_admin",
]


@ddt
class TestPreventGrandAdminAccess(SavepointCase):
    """Test that a light admin user may not grant admin priviledges."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.admin = cls.env.ref("base.user_demo")
        cls.admin.groups_id = cls.env.ref(
            "admin_light_user.group_user_management"
        ) | cls.env.ref("base.group_user")

        cls.user = cls.env["res.users"].create(
            {
                "name": "Basic User",
                "login": "basic_user",
            }
        )

    def test_onWrite_ifGrantEmployeeAccess_thenAccessErrorNotRaised(self):
        self.user.with_user(self.admin).write(
            {
                "groups_id": [(4, self.env.ref("base.group_user").id)],
            }
        )

    @data(*ADMIN_GROUPS)
    def test_onWrite_ifGrantAdmin_thenRaiseAccessError(self, admin_group):
        with pytest.raises(AccessError):
            self.user.with_user(self.admin).write(
                {
                    "groups_id": [(4, self.env.ref(admin_group).id)],
                }
            )

    def test_onCreate_ifGrantEmployeeAccess_thenAccessErrorNotRaised(self):
        self.env["res.users"].with_user(self.admin).create(
            {
                "name": "Basic User 2",
                "login": "basic_user_2",
                "email": "basic_user_2@example.com",
                "groups_id": [(4, self.env.ref("base.group_user").id)],
            }
        )

    @data(*ADMIN_GROUPS)
    def test_onCreate_ifGrantAdmin_thenRaiseAccessError(self, admin_group):
        with pytest.raises(AccessError):
            self.env["res.users"].with_user(self.admin).create(
                {
                    "name": "Basic User 2",
                    "login": "basic_user_2",
                    "email": "basic_user_2@example.com",
                    "groups_id": [(4, self.env.ref(admin_group).id)],
                }
            )

    def test_onWrite_withGroupList_ifGrantEmployeeAccess_thenAccessErrorNotRaised(self):
        self.user.with_user(self.admin).write(
            {
                "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
            }
        )

    @data(*ADMIN_GROUPS)
    def test_onWrite_withGroupList_ifGrantAdmin_thenRaiseAccessError(self, admin_group):
        groups = [self.env.ref("base.group_user").id, self.env.ref(admin_group).id]
        with pytest.raises(AccessError):
            self.user.with_user(self.admin).write(
                {
                    "groups_id": [(6, 0, groups)],
                }
            )

    def test_onCreate_withGroupList_ifGrantEmployeeAccess_thenAccessErrorNotRaised(
        self,
    ):
        self.env["res.users"].with_user(self.admin).create(
            {
                "name": "Basic User 2",
                "login": "basic_user_2",
                "email": "basic_user_2@example.com",
                "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
            }
        )

    @data(*ADMIN_GROUPS)
    def test_onCreate_withGroupList_ifGrantAdmin_thenRaiseAccessError(
        self, admin_group
    ):
        groups = [self.env.ref("base.group_user").id, self.env.ref(admin_group).id]
        with pytest.raises(AccessError):
            self.env["res.users"].with_user(self.admin).create(
                {
                    "name": "Basic User 2",
                    "login": "basic_user_2",
                    "email": "basic_user_2@example.com",
                    "groups_id": [(6, 0, groups)],
                }
            )

    def test_can_not_unarchive_super_admin(self):
        self.user.groups_id |= self.env.ref("base.group_erp_manager")
        with pytest.raises(AccessError):
            self.user.with_user(self.admin).active = True

    def test_can_unarchive_non_admin_user(self):
        self.user.with_user(self.admin).active = True
