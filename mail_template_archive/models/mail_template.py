# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    active = fields.Boolean(string='Active', default=True)

