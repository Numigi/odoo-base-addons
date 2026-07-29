# Copyright 2024 Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class BaseTranslate(models.Model):
    # Use a distinct model name to prevent conflicts with account_fr_ca_labels
    _name = "base.translate"
    _description = "Database Translation Terms (FR to CA)"



    lang_id = fields.Many2one(
        comodel_name="res.lang",
        default=lambda self: self.env["res.lang"].search([("code", "=", "fr_FR")], limit=1),
        string="Language")
    model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Model",
        ondelete="cascade",
        help="Leave empty to apply globally across all models.",
    )
    term_fr = fields.Char(string="Term Fr", required=True)
    term_ca = fields.Char(string="Term CA", required=True)

    def action_apply_translations(self):
        # Force translation updates from installed modules
        installed_modules = self._get_installed_modules()
        installed_modules._update_translations(["fr_FR"], True)
        self.env.registry.clear_cache()
        return self._build_success_notification()

    def _get_installed_modules(self):
        # Retrieve all currently installed modules
        return self.env["ir.module.module"].search([("state", "=", "installed")])

    def _build_success_notification(self):
        # Build standard Odoo notification dictionary
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Success",
                "message": "Translations applied successfully.",
                "type": "success",
                "sticky": False,
            },
        }

    def get_mapping_for_model(self, model_name):
        # Retrieve translation mapping targeting the specific model or globally
        domain = [
            "|",
            ("model_id", "=", False),
            ("model_id.model", "=", model_name),
        ]
        return {
            record.term_fr: record.term_ca
            for record in self.search(domain)
        }
