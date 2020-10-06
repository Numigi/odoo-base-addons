# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailBot(models.AbstractModel):

    _inherit = "mail.bot"

    def _is_bot_pinged(self, *args, **kwargs):
        return False
