# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class URLLinkType(models.Model):

    _name = 'url.link.type'
    _description = 'URL Link Type'
    _order = 'sequence'

    sequence = fields.Integer()
    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(default=True)
