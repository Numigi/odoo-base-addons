# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class MailThread(models.AbstractModel):

    _inherit = 'mail.thread'

    def _notify_get_recipients_classify(self, *args, **kwargs):
        res = super()._notify_get_recipients_classify(*args, **kwargs)
        for data in res:
            data['actions'] = []
        return res
