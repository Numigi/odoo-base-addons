# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import api, models

_logger = logging.getLogger(__name__)


class Prod2x(models.AbstractModel):

    _inherit = "prod2x"

    @api.model
    def run(self):
        super().run()
        self._activate_users()

    def _activate_users(self):
        _logger.info("Running user activation")
        group = self.env.ref("prod2x_user_activation.group_prod2x_activation")
        users_to_activate = self.env["res.users"].search(
            [("active", "=", False), ("groups_id", "=", group.id),]
        )
        for user in users_to_activate:
            self._activate_user(user)

    def _activate_user(self, user):
        _logger.info(f"Activating user {user.login}")
        user.active = True
