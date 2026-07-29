# Copyright 2026-today Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Canada French Labels",
    "version": "18.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Accounting",
    "summary": "Sanitize the accounting terms for Canada French",
    "depends": ["base", "lang_fr_activated"],
    "data": [
        "security/ir.model.access.csv",
        "data/base_translate.csv",
        "views/base_translate.xml",
    ],
    "installable": True,
    "auto-install": True,
    "post_init_hook": "post_init_hook",
}
