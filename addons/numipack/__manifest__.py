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
        # Numigi/odoo-base
        # 'admin_light_auditlog',  # TA#3892
        'admin_light_calendar',  # TA#3892
        'admin_light_mail',  # TA#3892
        'admin_light_base',  # TA#4894
        'admin_light_user',  # TA#4894

        # OCA/server-tools
        # 'base_technical_features',

        # OCA/server-ux
        # 'mass_editing',  # TA#4119

        # odoo/odoo
        'board',
        'document',  # TA#3415

        # OCA/server_brand
        # 'disable_odoo_online',

        # OCA/server-auth
        # 'password_security',  # TA#2532

        # Numigi/aeroo_reports
        # 'report_aeroo',

        # Numigi/odoo-web-addons
        # 'web_contextual_search_favorite',  # TA#2637
        # 'web_custom_label',  # TA#3928
        # 'web_search_date_range',
        # 'disable_quick_create',

        # OCA/web
        # 'web_search_with_and',  # TA#2547
    ],
    'data': [
        'admin_light_user_password_security_binding.xml',
    ],
    'installable': True,
}
