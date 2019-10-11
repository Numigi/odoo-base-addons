# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numipack Accounting',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Functional dependencies for all Odoo instances using accounting.',
    'depends': [
        # Numigi/odoo-base-addons
        'base_extended_security',

        # Numigi/odoo-account-addons
        'account_bank_menu',
        'account_fr_ca_labels',
        'account_invoice_check_total',
        'account_move_chatter',
        'account_negative_debit_credit',
        'account_payment_cancel_group',
        'invoice_currency_validation',
        'vendor_invoice_full_list',

        # Numigi/aeroo_reports
        'account_check_printing_aeroo',
    ],
    'data': [
        'security/extended_security_rule.xml',
    ],
    'installable': True,
}
