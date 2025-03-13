# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _default_groups(self):
        default_user_rights = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("base_setup.default_user_rights")
        )
        return super()._default_groups() if default_user_rights else []

    groups_id = fields.Many2many(default=_default_groups)
