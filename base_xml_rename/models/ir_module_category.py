# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class ModuleCategory(models.Model):

    _inherit = ('ir.module.category', 'xml.rename.mixin')
    _name = 'ir.module.category'
