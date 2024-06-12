# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numitech',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'summary': 'Quality tools we want in every instances.',
    'depends': [
        # Numigi/odoo-base
        'database_bi_user',
        'web_base_url_freeze',

        # OCA/server-tools
        'auto_backup',
    ],
    'data': [
        'data/db_backup.xml',
    ],
    'installable': True,
}
