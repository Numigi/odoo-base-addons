# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AuthOAuthProvider(models.Model):

    _inherit = 'auth.oauth.provider'

    response_type = fields.Char(string='Response Type')
