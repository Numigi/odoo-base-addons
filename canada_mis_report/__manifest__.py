# Copyright 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Canada MIS Builder Reports",
    "version": "16.0.1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Add MIS Builder Reports for Canada",
    "depends": [
        # OCA/mis-builder
        "mis_builder",
        # Numigi/odoo-account-addons
        "canada_account_types",
        "account_closing_journal_mis_builder",
        # Numigi/odoo-base
        "lang_fr_activated",
        # Odoo
        "l10n_ca",
    ],
    "data": [
        "data/mis_report_style.xml",
        "data/mis_report.xml",
    ],
    "installable": True,
}
