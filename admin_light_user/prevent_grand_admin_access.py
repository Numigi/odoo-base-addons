# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, _
from odoo.exceptions import AccessError

ADMIN_GROUPS = [
    'base.group_erp_manager',
    'base.group_system',
    'admin_light_base.group_admin',
]


class UsersWithNotGrantAdminAccessConstraint(models.Model):

    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        if self.env.user.has_group('admin_light_user.group_user_management'):
            self._check_not_granting_admin_priviledges(vals)

        return super().create(vals)

    @api.multi
    def write(self, vals):
        if self.env.user.has_group('admin_light_user.group_user_management'):
            self._check_not_granting_admin_priviledges(vals)

        return super().write(vals)

    def _check_not_granting_admin_priviledges(self, vals):
        groups_id = vals.get('groups_id', [])

        admin_group_ids = {self.env.ref(group_ref).id for group_ref in ADMIN_GROUPS}

        is_granting_admin = any(
            (command[0] == 4 and command[1] in admin_group_ids) or
            (command[0] == 6 and set(command[2]) & admin_group_ids)
            for command in groups_id
        )

        if is_granting_admin:
            raise AccessError(_(
                'You are not authorized to grant admin priviledges. '
                'Only the super admin can.'
            ))
