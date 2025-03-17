# Copyright 2025-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Canada French Labels",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "AGPL-3",
    "category": "Accounting",
    "summary": "Sanitize the accounting terms for Canada French",
    "depends": ["lang_fr_activated"],
    "data": [
        "data/translate.term.fr_ca.csv",
        "data/ir_config_parameter_data.xml",
        "security/ir.model.access.csv",
        "views/translate_term_fr_ca.xml",
    ],
    "installable": True,
    "auto-install": True,
}
