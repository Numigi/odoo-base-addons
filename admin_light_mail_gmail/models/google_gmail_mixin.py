# © 204 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

AUTHORIZED_GROUPS = "base.group_system,admin_light_mail.group_email_server"


class GoogleGmailMixin(models.AbstractModel):
    _inherit = 'google.gmail.mixin'

    google_gmail_authorization_code = fields.Char(groups=AUTHORIZED_GROUPS)
    google_gmail_refresh_token = fields.Char(groups=AUTHORIZED_GROUPS)
    google_gmail_access_token = fields.Char(groups=AUTHORIZED_GROUPS)
    google_gmail_access_token_expiration = fields.Integer(
        groups=AUTHORIZED_GROUPS)
    google_gmail_uri = fields.Char(groups=AUTHORIZED_GROUPS)
