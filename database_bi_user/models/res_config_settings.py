# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    database_bi_user_password = fields.Char()
    database_bi_user_disable_column_protection = fields.Boolean()

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            database_bi_user_disable_column_protection=self._is_bi_column_protection_disabled(),
        )
        return res

    def set_values(self):
        super().set_values()
        bi_user_pool = self.env["database.bi.user.update"]

        if self.database_bi_user_password:
            bi_user_pool.set_password(self.database_bi_user_password)

        if self._should_disable_column_protection():
            bi_user_pool.disable_column_protection()
        elif self._should_enable_column_protection():
            bi_user_pool.enable_column_protection()

    def _should_disable_column_protection(self):
        return (
            self.database_bi_user_disable_column_protection and
            not self._is_bi_column_protection_disabled()
        )

    def _should_enable_column_protection(self):
        return (
            not self.database_bi_user_disable_column_protection and
            self._is_bi_column_protection_disabled()
        )

    def _is_bi_column_protection_disabled(self):
        return self.env["database.bi.user.update"].is_column_protection_disabled()
