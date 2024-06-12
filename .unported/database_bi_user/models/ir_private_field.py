# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


def _update_bi_user(env):
    env['database.bi.user.update'].setup_role()


class PrivateField(models.Model):
    """Update the BI user when a change is made to private fields."""

    _inherit = 'ir.private.field'

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        _update_bi_user(self.env)
        return res

    def write(self, vals):
        res = super().write(vals)
        _update_bi_user(self.env)
        return res

    def unlink(self):
        res = super().unlink()
        _update_bi_user(self.env)
        return res
