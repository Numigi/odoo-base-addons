# Copyright 2024 Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class BaseTranslationCA(models.AbstractModel):
    _inherit = "base"

    def action_translate_to_ca(self):
        # Main entry point to transpose FR translations to CA for any existing model
        mapping_dict = self._get_ca_translation_mapping()
        translatable_fields = self._get_translatable_fields()
        self._apply_ca_translations_to_records(translatable_fields, mapping_dict)

    def _get_ca_translation_mapping(self):
        # Fetch dictionary mapping from the newly isolated translation term model
        term_model = self.env["base.translate"]
        return term_model.get_mapping_for_model(self._name)

    def _get_translatable_fields(self):
        # Identify translatable fields declared on the current model
        return [
            field_name
            for field_name, field_def in self._fields.items()
            if field_def.translate
        ]

    def _apply_ca_translations_to_records(self, fields_list, mapping_dict):
        # Iterate over recordset without exceeding two indentation levels
        for record in self:
            record._translate_record_fields(fields_list, mapping_dict)

    def _translate_record_fields(self, fields_list, mapping_dict):
        # Iterate over translatable fields for a single record
        for field_name in fields_list:
            self._translate_single_field(field_name, mapping_dict)

    def _translate_single_field(self, field_name, mapping_dict):
        # Read FR text and apply Canadian French mapping if value is string
        fr_value = self.with_context(lang="fr_FR")[field_name]
        if isinstance(fr_value, str):
            ca_value = self._replace_terms_in_text(fr_value, mapping_dict)
            self._write_ca_value(field_name, ca_value)

    def _replace_terms_in_text(self, text_value, mapping_dict):
        # Apply string replacements sorted by length descending
        sorted_keys = sorted(
            mapping_dict.keys(),
            key=lambda k: len(str(k)),
            reverse=True,
        )
        for old_term in sorted_keys:
            text_value = self._replace_single_term(text_value, old_term, mapping_dict)
        return text_value

    def _replace_single_term(self, text_value, old_term, mapping_dict):
        # Safe string replacement avoiding break or continue statements
        if old_term and str(old_term) in text_value:
            text_value = text_value.replace(
                str(old_term),
                str(mapping_dict[old_term]),
            )
        return text_value

    def _write_ca_value(self, field_name, ca_value):
        # Write translated value explicitly into the Canadian French language context
        self.with_context(lang="fr_CA").write({field_name: ca_value})
