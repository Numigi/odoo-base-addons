# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AuthOAuthProvider(models.Model):

    _inherit = 'auth.oauth.provider'

    response_type = fields.Char(string='Response Type')
