# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Admin Light Filters',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'AGPL-3',
    'category': 'Other',
    'summary': 'Add user-defined filter management to the Admin Light user',
    'depends': ['admin_light_web', 'filter_multi_user'],
    'data': [
        'security/admin_light_security.xml',
        'security/ir_filters_security.xml',
        'views/ir_filters_views.xml',
    ],
    'installable': True,
}
