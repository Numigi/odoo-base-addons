# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MailMessage(models.Model):

    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        message = super().create(vals)
        message._propagate_author_to_email_from()
        return message

    
    def write(self, vals):
        result = super().write(vals)

        if vals.get('email_from') or vals.get('author_idgs'):
            self._propagate_author_to_email_from()

        return result

    def _propagate_author_to_email_from(self):
        odoobot = self.env.ref("base.user_root").sudo()
        messages_to_propagate = self.filtered(
            lambda m: m.author_id.email and odoobot.email in m.email_from
        )
        for message in messages_to_propagate:
            author = message.author_id
            expected_email_from = "{} <{}>".format(author.name, author.email)
            if expected_email_from != message.email_from:
                message.email_from = expected_email_from
