# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MailBot(models.AbstractModel):

    _inherit = "mail.bot"

    def _is_bot_pinged(self, *args, **kwargs):
        return False
