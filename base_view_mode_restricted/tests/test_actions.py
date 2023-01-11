# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestViewModeRestrictions(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env.ref("base.user_admin")
        cls.group_1 = cls.env["res.groups"].create({"name": "Group 1"})
        cls.action = cls.env.ref("base.action_partner_form")

    def test_user_without_group(self):
        self.user.groups_id -= self.group_1
        self._setup_restriction("kanban", self.group_1)
        modes = self._get_authorized_view_modes()
        assert "kanban" not in modes

    def test_user_with_group(self):
        self.user.groups_id |= self.group_1
        self._setup_restriction("kanban", self.group_1)
        modes = self._get_authorized_view_modes()
        assert "kanban" in modes

    def test_multiple_restrictions(self):
        self.user.groups_id -= self.group_1
        self._setup_restriction("kanban,list", self.group_1)
        modes = self._get_authorized_view_modes()
        assert "kanban" not in modes
        assert "list" not in modes
        assert "form" in modes

    def test_view_mode_with_extra_spaces(self):
        self.user.groups_id -= self.group_1
        self._setup_restriction(" kanban ", self.group_1)
        modes = self._get_authorized_view_modes()
        assert "kanban" not in modes

    def _setup_restriction(self, view_modes, groups):
        self.action.write(
            {
                "view_mode_restriction_ids": [
                    (
                        0,
                        0,
                        {
                            "view_modes": view_modes,
                            "group_ids": [(6, 0, groups.ids)],
                        },
                    )
                ]
            }
        )

    def _get_authorized_view_modes(self):
        return {v[1] for v in self.action.sudo(self.user).views}
