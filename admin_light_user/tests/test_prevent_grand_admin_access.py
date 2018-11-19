# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data

import pytest

from odoo.tests import common
from odoo.exceptions import AccessError
from ..prevent_grand_admin_access import ADMIN_GROUPS


@ddt
class TestPreventGrandAdminAccess(common.SavepointCase):
    """Test that a light admin user may not grant admin priviledges."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin = cls.env.ref('base.user_demo')
        cls.admin.groups_id = (
            cls.env.ref('admin_light_user.group_user_management') |
            cls.env.ref('base.group_user')
        )

        cls.user = cls.env['res.users'].create({
            'name': 'Basic User',
            'login': 'basic_user',
        })

    def test_onWrite_ifGrantEmployeeAccess_thenAccessErrorNotRaised(self):
        self.user.sudo(self.admin).write({
            'groups_id': [(4, self.env.ref('base.group_user').id)],
        })

    @data(*ADMIN_GROUPS)
    def test_onWrite_ifGrantAdmin_thenRaiseAccessError(self, admin_group):
        with pytest.raises(AccessError):
            self.user.sudo(self.admin).write({
                'groups_id': [(4, self.env.ref(admin_group).id)],
            })

    def test_onCreate_ifGrantEmployeeAccess_thenAccessErrorNotRaised(self):
        self.env['res.users'].sudo(self.admin).create({
            'name': 'Basic User 2',
            'login': 'basic_user_2',
            'email': 'basic_user_2@example.com',
            'groups_id': [(4, self.env.ref('base.group_user').id)],
        })

    @data(*ADMIN_GROUPS)
    def test_onCreate_ifGrantAdmin_thenRaiseAccessError(self, admin_group):
        with pytest.raises(AccessError):
            self.env['res.users'].sudo(self.admin).create({
                'name': 'Basic User 2',
                'login': 'basic_user_2',
                'email': 'basic_user_2@example.com',
                'groups_id': [(4, self.env.ref(admin_group).id)],
            })

    def test_onWrite_withGroupList_ifGrantEmployeeAccess_thenAccessErrorNotRaised(self):
        self.user.sudo(self.admin).write({
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
        })

    @data(*ADMIN_GROUPS)
    def test_onWrite_withGroupList_ifGrantAdmin_thenRaiseAccessError(self, admin_group):
        groups = [self.env.ref('base.group_user').id, self.env.ref(admin_group).id]
        with pytest.raises(AccessError):
            self.user.sudo(self.admin).write({
                'groups_id': [(6, 0, groups)],
            })

    def test_onCreate_withGroupList_ifGrantEmployeeAccess_thenAccessErrorNotRaised(self):
        self.env['res.users'].sudo(self.admin).create({
            'name': 'Basic User 2',
            'login': 'basic_user_2',
            'email': 'basic_user_2@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])],
        })

    @data(*ADMIN_GROUPS)
    def test_onCreate_withGroupList_ifGrantAdmin_thenRaiseAccessError(self, admin_group):
        groups = [self.env.ref('base.group_user').id, self.env.ref(admin_group).id]
        with pytest.raises(AccessError):
            self.env['res.users'].sudo(self.admin).create({
                'name': 'Basic User 2',
                'login': 'basic_user_2',
                'email': 'basic_user_2@example.com',
                'groups_id': [(6, 0, groups)],
            })
