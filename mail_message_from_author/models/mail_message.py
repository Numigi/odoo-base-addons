# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MailMessage(models.Model):

    _inherit = 'mail.message'

    def _propagate_autor_to_email_from(self):
        messages_with_author_emails = self.filtered(lambda m: m.author_id.email)
        for message in messages_with_author_emails:
            author = message.author_id
            expected_email_from = "{} <{}>".format(author.name, author.email)
            if expected_email_from != message.email_from:
                message.email_from = expected_email_from

    @api.model
    def create(self, vals):
        message = super().create(vals)
        message._propagate_autor_to_email_from()
        return message

    @api.multi
    def write(self, vals):
        result = super().write(vals)

        if vals.get('email_from') or vals.get('author_id'):
            self._propagate_autor_to_email_from()

        return result
