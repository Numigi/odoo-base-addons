from odoo import fields, models


class UtmSource(models.Model):
    _inherit = "utm.source"

    active = fields.Boolean(string="Active")
