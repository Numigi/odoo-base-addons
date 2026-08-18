# Copyright 2026 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import fields, models, api


class BaseTranslate(models.Model):
    _name = "base.translate"
    _description = "Database Translation Terms (FR to CA)"

    lang_id = fields.Many2one(
        comodel_name="res.lang",
        default=lambda self: self.env["res.lang"].search([("code", "=", "fr_FR")], limit=1),
        string="Language",
        required=True,
    )
    model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Model",
        ondelete="cascade",
        help="Facultatif : Laissez vide pour appliquer globalement (menus, formulaires, rapports).",
    )
    term = fields.Char(string="Label", required=True)
    new_term = fields.Char(string="New Label", required=True)

    def action_apply_translations(self):
        lang_codes = list(set(self.search([]).mapped("lang_id.code")))
        if not lang_codes:
            lang_codes = ["fr_FR"]
        installed_modules = self._get_installed_modules()
        installed_modules._update_translations(lang_codes, True)

        self.env.registry.clear_cache()
        return self._build_success_notification()

    def _get_installed_modules(self):
        return self.env["ir.module.module"].search([("state", "=", "installed")])

    def _build_success_notification(self):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Success",
                "message": "Tranlataions applied on all the system",
                "type": "success",
                "sticky": False,
            },
        }

    @api.model
    def get_mapping_for_model(self, model_name):
        """
        Retrieve translation mapping for a specific model.
        Fetches both global terms (model_id is False) and model-specific terms.
        """
        domain = [
            "|",
            ("model_id", "=", False),
            ("model_id.model", "=", model_name),
        ]
        records = self.search(domain)
        return self._format_mapping_dictionary(records)

    def _format_mapping_dictionary(self, records):
        """
        Format the recordset into a dictionary mapping old terms to new terms.
        """
        return {record.term: record.new_term for record in records}
