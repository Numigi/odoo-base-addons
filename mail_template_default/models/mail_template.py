# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class MailTemplate(models.Model):
    _inherit = "mail.template"

    is_default_template = fields.Boolean("Default Template")

    @api.constrains("is_default_template", "model_id")
    def _check_unique_default_template(self):
        for record in self:
            if (
                record.search_count(
                    [
                        ("is_default_template", "=", True),
                        ("model_id", "=", record.model_id.id),
                    ]
                )
                > 1
            ):
                raise ValidationError(
                    _(
                        "This object already has a default template associated. \n"
                        "You cannot assign more than one default template by object."
                    )
                )
