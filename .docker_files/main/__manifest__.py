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
        "base",
        "crm",  # module added for test purpose
        "admin_light_auditlog",
        "admin_light_base",
        "admin_light_bi_view_editor",
        "admin_light_calendar",
        "admin_light_company",
        "admin_light_gamification",
        "admin_light_mail",
        "admin_light_mail_outlook",
        "attachment_minio",
        "lang_fr_activated",
        "mail_notification_no_action_button",
        "mail_template_default",
        "test_http_request",
    ],
    "installable": True,
}
