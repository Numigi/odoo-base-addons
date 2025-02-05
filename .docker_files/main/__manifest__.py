# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Main Module",
    "version": "1.0.0",
    "author": "Numigi",
    "maintainer": "Numigi",
    "website": "https://www.numigi.com",
    "license": "LGPL-3",
    "category": "Other",
    "summary": "Install all addons required for testing.",
    "depends": [
        "account",  # module added for unit testing (base_extended_security)
        "admin_light_auditlog",
        "admin_light_base",
        "admin_light_bi_view_editor",
        "admin_light_calendar",
        "admin_light_company",
        "admin_light_gamification",
        "admin_light_mail",
        "admin_light_mail_gmail",
        "admin_light_mail_outlook",
        "admin_light_user",
        "admin_light_web",
        "admin_light_filters",
        "attachment_minio",
        "base_extended_security",
        "crm",  # module added for test purpose
        "currency_rate_update_boc",
        "database_bi_user",
        "lang_fr_activated",
        "mail_notification_no_action_button",
        "mail_template_default",
        "private_data_group",
        "test_http_request",
    ],
    "installable": True,
}
