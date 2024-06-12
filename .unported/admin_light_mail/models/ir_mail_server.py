# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

AUTHORIZED_GROUPS = "base.group_system,admin_light_mail.group_email_server"


class IrMailServer(models.Model):

    _inherit = "ir.mail_server"

    smtp_user = fields.Char(groups=AUTHORIZED_GROUPS)
    smtp_pass = fields.Char(groups=AUTHORIZED_GROUPS)
