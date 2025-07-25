# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MailBot(models.AbstractModel):

    _inherit = "mail.bot"

    def _is_bot_pinged(self, *args, **kwargs):
        return False
