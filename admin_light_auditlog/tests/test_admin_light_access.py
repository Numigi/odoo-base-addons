# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import AccessError
from odoo.tests import common


class TestAdminLightAccess(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = cls.env.ref('admin_light_auditlog.group_auditlogs')
        cls.user = cls.env['res.users'].create({
            'name': 'Test',
            'login': 'testauditlog@test.com',
            'email': 'testauditlog@test.com',
            'groups_id': [(4, cls.group.id)],
        })

        cls.rule = cls.env['auditlog.rule'].create({
            'name': 'Test',
            'model_id': cls.env.ref('base.model_ir_cron').id,
            'log_write': True,
            'log_unlink': True,
            'log_create': True,
        })

    def test_can_activate_audit_rule(self):
        self.rule.sudo(self.user).subscribe()
        assert self.rule.state == 'subscribed'

    def test_can_deactivate_audit_rule(self):
        self.rule.subscribe()
        assert self.rule.state == 'subscribed'
        self.rule.sudo(self.user).unsubscribe()
        assert self.rule.state == 'draft'

    def test_if_not_admin_light__can_not_activate_audit_rule(self):
        self.user.groups_id -= self.group
        with pytest.raises(AccessError):
            self.rule.sudo(self.user).subscribe()

    def test_if_not_admin_light__can_not_deactivate_audit_rule(self):
        self.rule.subscribe()

        self.user.groups_id -= self.group
        with pytest.raises(AccessError):
            self.rule.sudo(self.user).unsubscribe()
