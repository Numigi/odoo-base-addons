# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numipack',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Functional dependencies for all Odoo instances.',
    'depends': [
        'base_technical_features',
        'board',
        'disable_odoo_online',
        'disable_quick_create',
        'password_security',  # TA#2532
        'report_aeroo',
        'web_search_date_range',
        'web_search_with_and',  # TA#2547
    ],
    'installable': True,
}
