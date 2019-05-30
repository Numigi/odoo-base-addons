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
        # Numigi/odoo-account-addons
        'account_bank_menu',
        'account_invoice_check_total',
        'account_move_chatter',
        'account_negative_debit_credit',
        'invoice_currency_validation',
        'vendor_invoice_full_list',

        # Numigi/aeroo_reports
        'account_check_printing_aeroo',
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
