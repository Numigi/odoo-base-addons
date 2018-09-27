# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Admin Light User',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Add a group to manage user access.',
    'depends': ['admin_light_base'],
    'data': [
        'data.xml',
        'mask_admin_groups.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
