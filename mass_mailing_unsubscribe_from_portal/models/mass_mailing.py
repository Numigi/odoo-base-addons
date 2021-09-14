# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from werkzeug.urls import url_join, url_encode
from odoo import fields, models


class MassMailing(models.Model):

    _inherit = 'mail.mass_mailing'

    def _get_user_unsubscribe_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        partner = self.env.user.partner_id
        mailing = self.search([], limit=1)
        return url_join(
            base_url, 'mail/mailing/%(mailing_id)s/unsubscribe?%(params)s' % {
                'mailing_id': mailing.id,
                'params': url_encode({
                    'db': self.env.cr.dbname,
                    'res_id': partner.id,
                    'email': partner.email,
                    'token': mailing._unsubscribe_token(partner.id, partner.email),
                }),
            }
        )
