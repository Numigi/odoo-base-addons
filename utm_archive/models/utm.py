from odoo import fields, models


class UtmCampaign(models.Model):
    _inherit = "utm.campaign"

    active = fields.Boolean(string="Active")


class UtmSource(models.Model):
    _inherit = "utm.source"

    active = fields.Boolean(string="Active")
