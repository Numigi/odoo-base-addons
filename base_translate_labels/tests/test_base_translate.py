# Copyright 2024 Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestTranslationFrCa(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.term_model = cls.env["base.translate"]
        cls.partner_model = cls.env["res.partner"]
        cls._create_test_terms(cls)

    def _create_test_terms(self):
        # Create global and model-specific translation mappings
        self.term_model.create({
            "term": "facture",
            "new_term": "facture canadienne",
        })

    def test_translation_applied_to_record_field(self):
        # Validate that FR terms are properly transposed to CA
        partner = self._create_test_partner("Voici votre facture")
        partner.action_translate_to_ca()
        ca_value = partner.with_context(lang="fr_CA").comment
        self.assertEqual(ca_value, "Voici votre facture canadienne")

    def test_global_mapping_retrieval(self):
        # Validate fetching mapping dictionary globally
        mapping = self.term_model.get_mapping_for_model("res.partner")
        self.assertEqual(mapping.get("facture"), "facture canadienne")

    def _create_test_partner(self, comment_text):
        # Helper method to create a partner with FR context
        return self.partner_model.with_context(lang="fr_FR").create({
            "name": "Test Partner",
            "comment": comment_text,
        })