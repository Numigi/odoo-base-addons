# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from urllib.parse import urljoin
from odoo import fields, models


class StagingEnvironment(models.Model):

    _name = 'staging.environment'
    _description = "Staging Environment"
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    url = fields.Char("URL")
    client = fields.Char()
    level = fields.Selection(
        [
            ("lab", "Lab"),
            ("test", "Test"),
            ("ecom", "Ecom"),
        ],
        required=True,
        default="lab",
    )
    token = fields.Char()
    active = fields.Boolean(default=True)

    database_selector_url = fields.Char(compute="_compute_database_selector_url")

    def _compute_database_selector_url(self):
        for record in self:
            record.database_selector_url = urljoin(
                self.url, "/web/database/selector"
            )
