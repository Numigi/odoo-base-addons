# Copyright 2026 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestTranslationFrCa(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.term_model = cls.env["base.translate"]
        cls.partner_model = cls.env["res.partner"]
        cls._create_test_terms()

    @classmethod
    def _create_test_terms(cls):
        cls.term_model.create({
            "term": "facture",
            "new_term": "facture canadienne",
        })

    def test_translation_applied_to_record_field(self):
        partner = self._create_test_partner("Voici votre facture")
        partner.action_translate_to_ca()
        ca_value = partner.with_context(lang="fr_CA").comment
        self.assertEqual(ca_value, "Voici votre facture canadienne")

    def test_global_mapping_retrieval(self):
        mapping = self.term_model.get_mapping_for_model("res.partner")
        self.assertEqual(mapping.get("facture"), "facture canadienne")

    def _create_test_partner(self, comment_text):
        return self.partner_model.with_context(lang="fr_FR").create({
            "name": "Test Partner",
            "comment": comment_text,
        })
