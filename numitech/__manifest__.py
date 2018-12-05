# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numitech',
    'version': '1.1.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'summary': 'Quality tools we want in every instances.',
    'depends': [
        # OCA/server-tools
        'auto_backup',
    ],
    'data': [
        'data/db_backup.xml',
        'data/ir_config_parameter.xml',
    ],
    'installable': True,
}
