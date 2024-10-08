# Copyright 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Admin Light Web',
    'version': '16.0.1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Add email management to the Admin Light application.',
    'depends': [
        'admin_light_base',
        'web_custom_label',
        'web_search_date_range',
    ],
    'data': [
        'views/common.xml',
        'views/custom_labels.xml',
        'views/date_filters.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
