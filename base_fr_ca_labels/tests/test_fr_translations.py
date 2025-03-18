# Copyright 2025-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from ddt import ddt, data
from odoo.tests.common import TransactionCase


@ddt
class TestTranslation(TransactionCase):
    def setUp(self):
        """
        Set up context and initial data for tests, including creating translation terms.
        """
        super().setUp()
        self.lang = "fr_FR"
        self.context = {"lang": self.lang}

        self.translation_term = self.env["translate.term.fr_ca"].create(
            {"term_fr": "de la taxe perçue", "term_ca": "de la taxe non perçue"}
        )

    def activate_language(self, lang):
        """
        Activate the specified language by updating translations for installed modules.
        """
        modules = self.env["ir.module.module"].search([("state", "=", "installed")])
        modules._update_translations(lang, True)

    @data(
        ("refund_sequence", "Séquence dédiée aux notes de crédit"),
    )
    def test_field_description_translation(self, data):
        """
        Test if the field's description is correctly translated based on the provided language.
        """
        field_name, expected_translation = data
        self.activate_language(self.lang)
        result = (
            self.env["ir.model.fields"]
            .with_context(self.context)
            .search_read(
                domain=[("name", "=", field_name)],
                fields=["field_description"],
                limit=1,
            )
        )

        field_description = result[0].get("field_description", "") if result else ""
        self.assertEqual(
            field_description,
            expected_translation,
            f"Translation mismatch for field '{field_name}'.",
        )

    def test_translation_update_with_custom_term(self):
        """
        Test if the field description reflects the custom translation term update.
        """
        self.activate_language(self.lang)

        result = (
            self.env["ir.model.fields"]
            .with_context(self.context)
            .search_read(
                domain=[("name", "=", "account_cash_basis_base_account_id")],
                fields=["field_description"],
                limit=1,
            )
        )

        field_description = result[0].get("field_description", "") if result else ""
        self.assertEqual(
            field_description,
            "Compte de base de la taxe non perçue",
            "Translation mismatch for 'account_cash_basis_base_account_id'",
        )

    def test_translation_after_removing_custom_term(self):
        """
        Test if the field description reverts to the original translation.
        """
        self.translation_term.unlink()
        self.activate_language(self.lang)

        result = (
            self.env["ir.model.fields"]
            .with_context(self.context)
            .search_read(
                domain=[("name", "=", "account_cash_basis_base_account_id")],
                fields=["field_description"],
                limit=1,
            )
        )

        field_description = result[0].get("field_description", "") if result else ""
        self.assertEqual(
            field_description,
            "Compte de base de la taxe perçue",
            "Translation mismatch for 'account_cash_basis_base_account_id'",
        )
