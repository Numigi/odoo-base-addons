# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Admin Light Company',
    'version': '1.0.1',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Add companies to the admin light application',
    'depends': ['admin_light_base'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
    ],
    'installable': True,
}
