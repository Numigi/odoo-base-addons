import logging
import threading
import psycopg2
from odoo import api, SUPERUSER_ID, sql_db
from odoo.tools.translate import TranslationImporter as BaseTranslationImporter
from odoo.tools.translate import CodeTranslations as BaseCodeTranslations
from odoo.tools.misc import ReadonlyDict

_logger = logging.getLogger(__name__)

base_load_translation = BaseTranslationImporter._load
base_get_web_translations = BaseCodeTranslations.get_web_translations
base_get_python_translations = BaseCodeTranslations.get_python_translations


def _replace_term_in_string(value, old_term, new_term):
    if old_term and str(old_term) in value:
        return value.replace(str(old_term), str(new_term))
    return value


def _apply_mapping(value, mapping):
    if not isinstance(value, str):
        return value
    sorted_keys = sorted(mapping.keys(), key=lambda k: len(str(k)), reverse=True)
    for old_term in sorted_keys:
        value = _replace_term_in_string(value, old_term, mapping[old_term])
    return value


def replace_values(data_dict, mapping, target_lang):
    for key, value in data_dict.items():
        if isinstance(value, dict):
            replace_values(value, mapping, target_lang)
        elif key == target_lang and isinstance(value, str):
            try:
                data_dict[key] = _apply_mapping(value, mapping)
            except Exception as error:
                _logger.error("Failed mapping for key '%s': %s", key, error)
    return data_dict


def get_odoo_environment():
    db_name = getattr(threading.current_thread(), "dbname", None)

    if not db_name:
        try:
            # Essayer de lire depuis l'attribut db du thread (CLI / installation)
            db_obj = getattr(threading.current_thread(), "db", None)
            if hasattr(db_obj, "dbname"):
                db_name = db_obj.dbname
        except Exception:
            pass

    if not db_name:
        return None, None

    database = sql_db.db_connect(db_name)
    if database is None:
        return None, None
    db_cursor = database.cursor()
    environment = api.Environment(db_cursor, SUPERUSER_ID, {})
    return environment, db_cursor


def get_translation_mapping(environment, lang_code):
    mapping_dict = {}
    term_model = "base.translate"
    if environment and term_model in environment.registry.models:
        try:
            records = environment[term_model].search([("lang_id.code", "=", lang_code)])
            mapping_dict = {record.term: record.new_term for record in records}
        except psycopg2.errors.UndefinedTable:
            _logger.warning("Table %s not defined yet. Skipping.", term_model)
        except Exception as error:
            _logger.error("Database error while fetching mapping: %s", error)
    return mapping_dict


class TranslationImporter(BaseTranslationImporter):
    def _load(self, reader, lang, xmlids=None):
        base_load_translation(self, reader, lang, xmlids)
        mapping_dict = get_translation_mapping(self.env, lang)
        if mapping_dict:
            self.model_translations = replace_values(self.model_translations, mapping_dict, lang)
            self.model_terms_translations = replace_values(self.model_terms_translations, mapping_dict, lang)


def _process_python_translations(instance, module_name, lang):
    try:
        environment, db_cursor = get_odoo_environment()
        if not environment or not db_cursor:
            return
        mapping_dict = get_translation_mapping(environment, lang)
        db_cursor.close()
        if mapping_dict:
            orig = instance.python_translations.get((module_name, lang), {})
            new_dict = {src: _apply_mapping(val, mapping_dict) for src, val in orig.items()}
            instance.python_translations[(module_name, lang)] = ReadonlyDict(new_dict)
    except Exception as error:
        _logger.error("Error in python translations for %s: %s", module_name, error)


def _process_web_translations(instance, module_name, lang):
    try:
        environment, db_cursor = get_odoo_environment()
        if not environment or not db_cursor:
            return
        mapping_dict = get_translation_mapping(environment, lang)
        db_cursor.close()
        if mapping_dict:
            orig = instance.web_translations.get((module_name, lang), {})
            # On conserve scrupuleusement la structure du message Javascript
            new_messages = []
            for msg in orig.get("messages", ()):
                new_str = _apply_mapping(msg.get("string", ""), mapping_dict)
                new_messages.append(ReadonlyDict({
                    "id": msg["id"],
                    "string": new_str,
                }))
            instance.web_translations[(module_name, lang)] = ReadonlyDict({
                "messages": tuple(new_messages)
            })
    except Exception as error:
        _logger.error("Error in web translations for %s: %s", module_name, error)


class CodeTranslations(BaseCodeTranslations):
    def get_python_translations(self, module_name, lang):
        if (module_name, lang) not in self.python_translations:
            BaseCodeTranslations._load_python_translations(self, module_name, lang)
            _process_python_translations(self, module_name, lang)
        return self.python_translations[(module_name, lang)]

    def get_web_translations(self, module_name, lang):
        if (module_name, lang) not in self.web_translations:
            BaseCodeTranslations._load_web_translations(self, module_name, lang)
            _process_web_translations(self, module_name, lang)
        return self.web_translations[(module_name, lang)]


BaseTranslationImporter._load = TranslationImporter._load
BaseCodeTranslations.get_web_translations = CodeTranslations.get_web_translations
BaseCodeTranslations.get_python_translations = CodeTranslations.get_python_translations