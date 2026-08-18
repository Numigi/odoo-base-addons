# Copyright 2026 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class BaseTranslate(models.Model):
    _name = "translate.fr_ca"
    _description = "Database Translation Terms (FR to CA)"

    lang_id = fields.Many2one(
        comodel_name="res.lang",
        default=lambda self: self._get_default_lang(),
        string="Language",
        required=True,
    )
    model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Model",
        ondelete="cascade",
        help="Optional: Leave empty to apply globally (menus, forms, reports).",
    )
    term = fields.Char(string="Label", required=True)
    new_term = fields.Char(string="New Label", required=True)

    def _get_default_lang(self):
        return self.env["res.lang"].search([("code", "=", "fr_FR")], limit=1)

    def action_apply_translations(self):
        lang_codes = self._get_active_lang_codes()
        installed_modules = self._get_installed_modules()
        installed_modules._update_translations(lang_codes, True)
        self.env.registry.clear_cache()
        return self._build_success_notification()

    def _get_active_lang_codes(self):
        codes = list(set(self.search([]).mapped("lang_id.code")))
        if not codes:
            codes = ["fr_FR"]
        return codes

    def _get_installed_modules(self):
        return self.env["ir.module.module"].search([("state", "=", "installed")])

    def _build_success_notification(self):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Success",
                "message": "Translations applied on all the system",
                "type": "success",
                "sticky": False,
            },
        }

    @api.model
    def get_mapping_for_model(self, model_name):
        domain = [
            "|",
            ("model_id", "=", False),
            ("model_id.model", "=", model_name),
        ]
        records = self.search(domain)
        return self._format_mapping_dictionary(records)

    def _format_mapping_dictionary(self, records):
        return {record.term: record.new_term for record in records}
