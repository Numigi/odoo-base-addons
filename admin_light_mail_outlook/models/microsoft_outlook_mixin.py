# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

AUTHORIZED_GROUPS = "base.group_system,admin_light_mail.group_email_server"


class MicrosoftOutlookMixin(models.AbstractModel):
    _inherit = 'microsoft.outlook.mixin'

    microsoft_outlook_refresh_token = fields.Char(groups=AUTHORIZED_GROUPS)
    microsoft_outlook_access_token = fields.Char(groups=AUTHORIZED_GROUPS)
    microsoft_outlook_access_token_expiration = fields.Integer(
        groups=AUTHORIZED_GROUPS)
    microsoft_outlook_uri = fields.Char(groups=AUTHORIZED_GROUPS)
