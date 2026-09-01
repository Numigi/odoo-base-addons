# Copyright 2026-today Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Base Translation Manager",
    "version": "18.0.1.2.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Accounting",
    "summary": "This module provides a generic and robust toolset to manage translations across the entire "
               "Odoo database.",
    "depends": ["base", "lang_fr_activated"],
    "data": [
        "security/ir.model.access.csv",
        "views/base_translate.xml",
        "wizard/data_tanslation_wizard.xml"
    ],
    "installable": True,
    "auto-install": True,
    "post_init_hook": "post_init_hook",
}
