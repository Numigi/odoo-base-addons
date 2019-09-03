# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    database_bi_user_password = fields.Char()

    @api.multi
    def set_values(self):
        super().set_values()
        if self.database_bi_user_password:
            self.env['database.bi.user.update'].set_password(self.database_bi_user_password)
