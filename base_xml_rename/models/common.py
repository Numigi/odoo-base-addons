# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


def is_lang_installed(env: 'Environment', lang: str):
    return lang in dict(env['res.lang'].get_installed())


def rename_record(record: 'base', lang: str, value: str):
    record.with_context(lang=lang).name = value
