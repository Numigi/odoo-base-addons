# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrAttachment(models.Model):

    _inherit = 'ir.attachment'

    res_id = fields.Integer(readonly=False)
    res_model = fields.Char(readonly=False)
    res_field = fields.Char(readonly=False)
