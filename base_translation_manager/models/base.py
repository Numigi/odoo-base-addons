# Copyright 2026 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from odoo import models


class BaseTranslationCA(models.AbstractModel):
    _inherit = "base"

    def action_translate_to_ca(self):
        mapping_dict = self._get_ca_translation_mapping()
        translatable_fields = self._get_translatable_fields()
        self._apply_ca_translations_to_records(translatable_fields, mapping_dict)

    def _get_ca_translation_mapping(self):
        term_model = self.env["base.translate"]
        return term_model.get_mapping_for_model(self._name)

    def _get_translatable_fields(self):
        return [
            field_name
            for field_name, field_def in self._fields.items()
            if field_def.translate
        ]

    def _apply_ca_translations_to_records(self, fields_list, mapping_dict):
        for record in self:
            record._translate_record_fields(fields_list, mapping_dict)

    def _translate_record_fields(self, fields_list, mapping_dict):
        for field_name in fields_list:
            self._translate_single_field(field_name, mapping_dict)

    def _translate_single_field(self, field_name, mapping_dict):
        fr_value = self.with_context(lang="fr_FR")[field_name]
        if isinstance(fr_value, str):
            ca_value = self._replace_terms_in_text(fr_value, mapping_dict)
            self._write_ca_value(field_name, ca_value)

    def _replace_terms_in_text(self, text_value, mapping_dict):
        sorted_keys = sorted(
            mapping_dict.keys(),
            key=lambda k: len(str(k)),
            reverse=True,
        )
        for old_term in sorted_keys:
            text_value = self._replace_single_term(text_value, old_term, mapping_dict)
        return text_value

    def _replace_single_term(self, text_value, old_term, mapping_dict):
        if not old_term:
            return text_value
        pattern = re.compile(re.escape(str(old_term)), re.IGNORECASE)
        return pattern.sub(
            lambda match: self._match_case_format(match.group(0), str(mapping_dict[old_term])),
            text_value
        )

    def _match_case_format(self, original_text, new_text):
        if original_text.isupper():
            return new_text.upper()
        if original_text.islower():
            return new_text.lower()
        return self._match_capitalized(original_text, new_text)

    def _match_capitalized(self, original_text, new_text):
        if original_text and original_text[0].isupper():
            return self._capitalize_first_letter(new_text)
        return new_text

    def _capitalize_first_letter(self, text):
        if not text:
            return text
        return text[0].upper() + text[1:]

    def _write_ca_value(self, field_name, ca_value):
        self.with_context(lang="fr_CA").write({field_name: ca_value})
