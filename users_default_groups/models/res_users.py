# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _default_groups(self):
        default_user_rights = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("base_setup.default_user_rights", "0")
        )

        # Convert 0 and 1 to boolean
        default_user_rights = bool(int(default_user_rights))

        if default_user_rights:
            return super()._default_groups()
        return [(6, 0, [self.env.ref("base.group_user").id])]

    groups_id = fields.Many2many(default=_default_groups)
