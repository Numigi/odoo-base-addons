# Copyright 2026 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


class TestTranslationFrCa(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_test_languages()
        cls.term_model = cls.env["base.translate"]
        cls.category_model = cls.env["res.partner.category"]
        cls._create_test_terms()

    @classmethod
    def _setup_test_languages(cls):
        cls._activate_language("fr_FR", "French")
        cls._activate_language("fr_CA", "French (Canada)")

    @classmethod
    def _activate_language(cls, code, name):
        lang = cls.env["res.lang"].with_context(active_test=False).search([("code", "=", code)])
        if lang:
            lang.write({"active": True})
        else:
            cls._create_language(code, name)

    @classmethod
    def _create_language(cls, code, name):
        cls.env["res.lang"].create({
            "name": name,
            "code": code,
            "url_code": code.replace("_", "-").lower(),
        })

    @classmethod
    def _create_test_terms(cls):
        cls.term_model.create({
            "term": "devis",
            "new_term": "soumission",
        })

    def test_translation_applied_with_dynamic_case_preservation(self):
        category = self._create_test_category("Mon Devis est un devis DEVIS")
        category.action_translate_to_ca()
        ca_value = category.with_context(lang="fr_CA").name
        self.assertEqual(ca_value, "Mon Soumission est un soumission SOUMISSION")

    def test_global_mapping_retrieval(self):
        mapping = self.term_model.get_mapping_for_model("res.partner.category")
        self.assertEqual(mapping.get("devis"), "soumission")

    def _create_test_category(self, name_text):
        return self.category_model.with_context(lang="fr_FR").create({
            "name": name_text,
        })
