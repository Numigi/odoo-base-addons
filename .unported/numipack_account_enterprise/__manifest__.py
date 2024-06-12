# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numipack Accounting',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Functional dependencies for all Odoo instances using enterprise accounting.',
    'depends': [
        # odoo/enterprise
        'account_accountant',

        # Numigi/odoo-account-addons
        'account_report_line_menu',
    ],
    'installable': True,
}
