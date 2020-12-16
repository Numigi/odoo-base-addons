# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import SavepointCase


class TestUserActivation(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = cls.env.ref("prod2x_user_activation.group_prod2x_activation")
        cls.user = cls.env["res.users"].create(
            {
                "name": "test@example.com",
                "email": "test@example.com",
                "login": "test@example.com",
                "prod2x_activation": True,
                "active": False,
                "groups_id": [(4, cls.group.id)],
            }
        )

    def test_activation_enabled(self):
        assert not self.user.active
        self.env["prod2x"].run()
        assert self.user.active

    def test_activation_disabled(self):
        assert not self.user.active
        self.user.groups_id -= self.group
        self.env["prod2x"].run()
        assert not self.user.active
