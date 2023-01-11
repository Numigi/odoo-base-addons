from odoo import fields, models


class UtmCampaign(models.Model):
    _inherit = "utm.campaign"

    active = fields.Boolean(string="Active")