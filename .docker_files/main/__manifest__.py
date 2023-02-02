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
        "auth_oauth_authentik",
        "automatic_activity_deadlines",
        "base_extended_security",
        "base_extended_security_grid",
        #"base_extended_security_test",
        "base_selection_label",
        "base_view_mode_restricted",
        "base_xml_rename",
        #"helpdesk_ticket_phone",
        "ir_attachment_access_token_portal",
        "ir_attachment_name_autocomplete",
       # "lang_fr_activated",
        "mail_activity_list_mark_done",
        "mail_activity_not_deleted",
        "mail_bot_no_pong",
       # "mail_follower_picker",
        "mail_notification_no_action_button",
        "mail_message_from_author",
        "mail_notification_no_footer",
        #"mail_template_archive",
        "mail_template_default",
        "note_no_default_stage",
        "private_data_group",
        "queue_job_auto_requeue",
        #"url_link_type",
        "test_http_request",
        "utm_archive",
        "web_email_field_new_tab",
    ],
    "installable": True,
}
