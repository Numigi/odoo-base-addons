# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Konvergo',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Dependencies for Konvergo',
    'depends': [
        # Numigi/odoo-base
        'numipack',
        'odoo-debrand',  # TA#16526

        # OCA/social
        'mail_debrand',  # TA#16549
    ],
    'installable': True,
}
