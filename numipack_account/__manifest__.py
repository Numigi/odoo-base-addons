# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numipack Accounting',
    'version': '1.2.2',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Functional dependencies for all Odoo instances using accounting.',
    'depends': [
        'numipack',

        # Numigi/odoo-base-addons
        'base_extended_security',

        # Numigi/odoo-account-addons
        'account_bank_menu',
        'account_fr_ca_labels',
        'account_fiscalyear_end_on_company',  # TA#58024
        # 'account_invoice_check_total',
        'account_move_reversal_access',  # TA#33729
        'account_move_unique_reversal',  # TA#33729
        'account_negative_debit_credit',
        'account_payment_cancel_group',
        'invoice_currency_validation',

        # Numigi/aeroo_reports
        'account_check_printing_aeroo',

        # Numigi/web-addons
        'web_search_date_range_account',
    ],
    'data': [
        'data/auditlog_rule.xml',
        'security/extended_security_rule.xml',
        'views/res_company.xml',
    ],
    'installable': True,
}
