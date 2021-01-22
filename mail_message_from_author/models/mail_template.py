# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MailTemplate(models.Model):

    _inherit = "mail.template"

    def send_mail(self, *args, **kwargs):
        if self.email_from:
            self = self.with_context(no_mail_from_author=True)
        return super(MailTemplate, self).send_mail(*args, **kwargs)
