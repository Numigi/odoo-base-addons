# -*- coding: utf-8 -*-
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numipack',
    'version': '1.0.4',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Functional dependencies for all Odoo instances.',
    'depends': [
        # Numigi/odoo-base
        'admin_light_auditlog',  # TA#3892
        'admin_light_calendar',  # TA#3892
        'admin_light_company',  # TA#19785
        'admin_light_filters',  # TA#52688
        'admin_light_mail',  # TA#3892
        'admin_light_base',  # TA#4894
        'admin_light_user',  # TA#4894
        'admin_light_web',  # TA#3892
        'prod2x',
        'prod2x_user_activation',

        # OCA/server-ux
        'base_technical_features',
        'mass_editing',  # TA#4119

        # odoo/odoo
        'auth_password_policy',  # TA#9918
        'board',
        # 'document',  # TA#3415
        'product',

        # OCA/server-brand
        'disable_odoo_online',

        # Numigi/aeroo_reports
        'report_aeroo',
        'report_aeroo_replace_qweb',

        # Numigi/odoo-partner-addons
        'contacts_config_menu_moved_right',  # TA#18504
        'partner_autocomplete_disable',  # TA#47076
        'partner_edit_group',  # TA#10975
        # 'partner_phone_validation',  # TA#5979

        # Numigi/odoo-base-addons
        'base_extended_security',
        'base_external_report_layout',  # TA#57998
        'ir_attachment_access_token_portal',  # TA#6109
        'mail_template_default',  # TA#21323
        'web_email_field_new_tab',  # TA#9753

        # Numigi/odoo-product-addons
        # 'product_extra_views',  # TA#15297

        # Numigi/odoo-web-addons
        'web_custom_label',  # TA#3928
        'web_custom_modifier',  # TA#16243
        'web_search_date_range',
        'disable_quick_create',

        # OCA/web
        'web_advanced_search',  # TA#53339
        'web_search_with_and',  # TA#2547 TA#53106

        # itpp-labs/sync-addons
        'base_automation_webhook',  # TA#56932 TA#59200

    ],
    'data': [
        'data/auditlog_rule.xml',
        'security/extended_security_rule.xml',
    ],
    'installable': True,
}
