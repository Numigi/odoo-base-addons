# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class MailThread(models.AbstractModel):

    _inherit = 'mail.thread'

    def _notify_classify_recipients(self, *args, **kwargs):
        res = super()._notify_classify_recipients(*args, **kwargs)
        for data in res:
            data['actions'] = []
        return res
