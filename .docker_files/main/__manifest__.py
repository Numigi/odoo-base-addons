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
        "crm",  # required for testing mail_notification_no_action_button
        "auditlog",
        "base_extended_security",
        "base_extended_security_grid",
        "base_view_mode_restricted",
        "base_xml_rename",
        "currency_rate_update_boc",
        "disable_install_from_website",
        "document_page_approval_no_mail",
        "helpdesk_mgmt_no_mail",
        "helpdesk_ticket_phone",
        "ir_attachment_access_token_portal",
        "ir_attachment_name_autocomplete",
        "ir_attachment_ressource_editable",
        "mail_activity_not_deleted",
        "mail_bot_no_pong",
        "mail_follower_picker",
        "mail_message_from_author",
        "mail_notification_no_action_button",
        "mail_notification_no_footer",
        "mail_recipient_unchecked",
        "mail_template_archive",
        "mail_template_default",
        "note_no_default_stage",
        "private_data_group",
        "queue_job_auto_requeue",
        "super_calendar",
        "url_link_type",
        "utm_archive",
        "web_email_field_new_tab",
    ],
    "installable": True,
}
