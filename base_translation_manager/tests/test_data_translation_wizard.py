# Copyright 2026-today Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestDataTranslationWizard(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._activate_test_languages()
        cls.source_lang = cls._get_language("fr_CA")
        cls.dest_lang = cls._get_language("fr_FR")
        cls.model_id = cls._get_model("res.partner.category")
        cls.test_record = cls._create_test_record()

    @classmethod
    def _activate_test_languages(cls):
        cls.env["res.lang"]._activate_lang("fr_CA")
        cls.env["res.lang"]._activate_lang("fr_FR")

    @classmethod
    def _get_language(cls, lang_code):
        return cls.env["res.lang"].search([("code", "=", lang_code)])

    @classmethod
    def _get_model(cls, model_name):
        return cls.env["ir.model"].search([("model", "=", model_name)])

    @classmethod
    def _create_test_record(cls):
        return cls.env["res.partner.category"].with_context(lang="fr_CA").create(
            {"name": "Catégorie Québécoise"}
        )

    def _create_wizard_for_all_records(self):
        return self.env["data.translation.wizard"].create(
            {
                "source_lang_id": self.source_lang.id,
                "dest_lang_id": self.dest_lang.id,
                "model_id": self.model_id.id,
                "operation": "copy",
                "data_option": "all",
                "record_domain": "[]",
            }
        )

    def _create_wizard_with_domain(self, domain_string):
        return self.env["data.translation.wizard"].create(
            {
                "source_lang_id": self.source_lang.id,
                "dest_lang_id": self.dest_lang.id,
                "model_id": self.model_id.id,
                "operation": "copy",
                "data_option": "selection",
                "record_domain": domain_string,
            }
        )

    def test_copy_operation_updates_destination_language(self):
        wizard = self._create_wizard_for_all_records()
        wizard.action_execute_operation()
        fr_name = self.test_record.with_context(lang="fr_FR").name
        assert fr_name == "Catégorie Québécoise"

    def test_domain_selection_filters_records_correctly(self):
        domain = f"[('id', '=', {self.test_record.id})]"
        wizard = self._create_wizard_with_domain(domain)
        records = wizard._get_target_records()
        assert self.test_record in records

    def test_domain_selection_excludes_unmatched_records(self):
        domain = "[('id', '=', 0)]"
        wizard = self._create_wizard_with_domain(domain)
        records = wizard._get_target_records()
        assert not records
