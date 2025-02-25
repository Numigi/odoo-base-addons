# Copyright 2024 Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


"""
Important Note:

This file overrides certain functions from the Odoo native tools/translate.py module.
To ensure compatibility with future Odoo updates, the original implementations of the
functions are retained and called within each overridden function. The original functions
are assigned to the following variables:
- base_get_python_translations
- base_get_web_translations
- base_load_translation

This approach allows us to customize the functionality while preserving the ability
to integrate updates from Odoo without losing any enhancements made in this module.
"""

import threading
import psycopg2

from odoo import api, SUPERUSER_ID, sql_db
from odoo.tools.translate import TranslationImporter as BaseTranslationImporter
from odoo.tools.translate import CodeTranslations as BaseCodeTranslations

base_load_translation = BaseTranslationImporter._load
base_get_web_translations = BaseCodeTranslations.get_web_translations
base_get_python_translations = BaseCodeTranslations.get_python_translations


def replace_values(data_dict, mapping, lang="fr_FR"):
    """
    Replace strings in the given dictionary based on
    the mapping provided for a specific language key.
    """

    def recursive_replace(current_dict):
        for key, value in current_dict.items():
            if isinstance(value, dict):
                recursive_replace(value)
            elif key == lang and isinstance(value, str):
                for old_term, new_term in mapping.items():
                    if old_term in value:
                        current_dict[key] = value.replace(old_term, new_term)
                        break

    recursive_replace(data_dict)
    return data_dict


def get_odoo_environment():
    """
    Retrieve the Odoo environment with a database cursor.
    """
    db_name = getattr(threading.current_thread(), "dbname", None)
    db_cursor = None
    environment = None
    if db_name:
        database = sql_db.db_connect(db_name)
        if database is not None:
            db_cursor = database.cursor()
            environment = api.Environment(db_cursor, SUPERUSER_ID, {})
    if environment is None or db_cursor is None:
        raise RuntimeError(
            "Failed to retrieve the Odoo environment or database cursor."
        )
    return environment, db_cursor


def get_translation_mapping(environment, module_name=False):
    """
    Retrieve the translation mapping dictionary for French (fr) to Canadian French (fr_CA).
    If a module name is provided, only mappings related to that module will be returned.
    """
    mapping_dict = {}
    if "translate.term.fr_ca" in environment.registry.models:
        try:
            domain = []
            # if module_name:
            #     domain.append(("modules.name", "=", module_name))

            records = environment["translate.term.fr_ca"].search(domain)
            mapping_dict = {record.term_fr: record.term_ca for record in records}

        except psycopg2.errors.UndefinedTable:
            # Skip if the mapping table is not yet created
            # (e.g., during initial module installation)
            pass

    return mapping_dict


class TranslationImporter(BaseTranslationImporter):
    def _load(self, reader, lang, xmlids=None):
        """
        Load and apply language-specific term replacements.
        """
        base_load_translation(self, reader, lang, xmlids)

        if lang == "fr_FR":
            mapping_dict = get_translation_mapping(self.env)

            if mapping_dict:
                self.model_translations = replace_values(
                    self.model_translations, mapping_dict
                )
                self.model_terms_translations = replace_values(
                    self.model_terms_translations, mapping_dict
                )


class CodeTranslations(BaseCodeTranslations):
    def get_web_translations(self, module_name, lang):
        BaseCodeTranslations._load_web_translations(self, module_name, lang)
        translations = base_get_web_translations(self, module_name, lang)
        if lang == "fr_FR":
            environment, db_cursor = get_odoo_environment()
            if environment:
                mapping_dict = get_translation_mapping(environment, module_name)

                for source, translated in translations.items():
                    for old_term, new_term in mapping_dict.items():
                        if old_term in translated:
                            translations[source] = translated.replace(
                                old_term, new_term
                            )
            if db_cursor:
                db_cursor.close()

        return translations

    def get_python_translations(self, module_name, lang):
        BaseCodeTranslations._load_python_translations(self, module_name, lang)
        translations = base_get_python_translations(self, module_name, lang)

        if lang == "fr_FR":
            environment, db_cursor = get_odoo_environment()
            if environment:
                mapping_dict = get_translation_mapping(environment, module_name)

                for source, translated in translations.items():
                    for old_term, new_term in mapping_dict.items():
                        if old_term in translated:
                            translations[source] = translated.replace(
                                old_term, new_term
                            )
            if db_cursor:
                db_cursor.close()
        return translations


BaseTranslationImporter._load = TranslationImporter._load
BaseCodeTranslations.get_web_translations = CodeTranslations.get_web_translations
BaseCodeTranslations.get_python_translations = CodeTranslations.get_python_translations
