# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        default_mail_template = self.env["mail.template"].search(
            [
                ("model_id.model", "=", self._context.get("default_model")),
                ("is_default_template", "=", True),
            ],
            limit=1,
        )
        if default_mail_template:
            res["template_id"] = default_mail_template.id
        return res
