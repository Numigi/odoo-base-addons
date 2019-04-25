# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class MailComposeMessageFollowers(models.TransientModel):
    """ Add the list of followers of the Mail message in the mail compose message wizard.
    Additionally, it passes the selected followers to send the mail by the context.
    """
    _inherit = 'mail.compose.message'

    def get_mail_followers(self, subtype_id=1):
        """ Given a mail message instance, return all the followers of the mail message

        :param models.Model self: mail.message instance
        :param int subtype_id: mail.message.subtype to check against followers;

        :rtype: recordset of res.partners
        """
        result = self.default_get(['model', 'res_id'])
        res_id = result['res_id']
        model = result['model']
        record = self.env[model].browse(res_id)
        followers_details = self.env['mail.followers']._get_recipient_data(record, subtype_id)
        return self.env['res.partner'].browse(details[0] for details in followers_details)

    follower_ids = fields.Many2many(
        'res.partner', 'mail_compose_message_res_partner_rel',
        'wizard_id', 'partner_id', 'Followers',
        default=get_mail_followers)

    @api.multi
    def action_send_mail(self):
        """ Pass the context "custom_followers" """
        self_with_context = self.with_context(custom_followers=self.follower_ids)
        return super(MailComposeMessageFollowers, self_with_context).action_send_mail()


class MailFollowersCustomFollowers(models.Model):
    """ Use the context item "custom_followers" to filter the partners to send the notification."""

    _inherit = 'mail.followers'

    def _get_recipient_data(self, *args, **kwargs):
        """ Filter the recipient using context variable."""
        res = super()._get_recipient_data(*args, **kwargs)
        follower_ids = self.env.context.get('custom_followers')
        if follower_ids:
            res = [r for r in res if r[0] in follower_ids.mapped('id')]
            _logger.info('Sending email to partial list of followers: %s', follower_ids)
        return res
