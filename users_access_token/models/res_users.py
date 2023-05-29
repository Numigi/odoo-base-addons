# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ['res.users', 'portal.mixin']
