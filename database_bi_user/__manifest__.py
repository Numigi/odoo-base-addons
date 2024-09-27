# Copyright 2019-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Database BI User',
    'version': '16.0.1.2.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Add a BI database user with restricted privileges',
    'depends': [
        'base_setup',
        'private_data_group',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/update.xml',
        'views/res_config_settings.xml',
    ],
    'installable': True,
}
