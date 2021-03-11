# © 2018 Numigi
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
        "account",  # required for testing auditlog
        "sale",  # required for testing mail_message_from_author
        "stock",  # required for testing base_extended_security
        "crm",  # required for testing mail_notification_no_action_button
        "auditlog",
        "base_extended_security",
        "base_extended_security_grid",
        "base_extended_security_test",
        "base_xml_rename",
        "helpdesk_ticket_phone",
        "ir_attachment_access_token_portal",
        "mail_activity_not_deleted",
        "mail_bot_no_pong",
        "mail_follower_picker",
        "mail_notification_no_action_button",
        "mail_notification_no_footer",
        "mail_template_archive",
        "mail_template_default",
        "note_no_default_stage",
        "private_data_group",
        "queue_job_auto_requeue",
        "url_link_type",
        "web_email_field_new_tab",
    ],
    "installable": True,
}
