# Copyright 2026 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestTranslationFrCa(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.term_model = cls.env["base.translate"]
        cls.category_model = cls.env["res.partner.category"]
        cls._create_test_terms()

    @classmethod
    def _create_test_terms(cls):
        cls.term_model.create({
            "term": "facture",
            "new_term": "facture canadienne",
        })

    def test_translation_applied_to_record_field(self):
        category = self._create_test_category("Voici votre facture")
        category.action_translate_to_ca()
        ca_value = category.with_context(lang="fr_CA").name
        self.assertEqual(ca_value, "Voici votre facture canadienne")

    def test_global_mapping_retrieval(self):
        mapping = self.term_model.get_mapping_for_model("res.partner.category")
        self.assertEqual(mapping.get("facture"), "facture canadienne")

    def _create_test_category(self, name_text):
        return self.category_model.with_context(lang="fr_FR").create({
            "name": name_text,
        })
