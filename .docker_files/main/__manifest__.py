# © 2018 Numigi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Main Module',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Install all addons required for testing.',
    'depends': [
        'account',  # required for testing auditlog
        'sale',  # required for testing mail_message_from_author

        'auditlog',
        'base_extended_security',
        'base_extended_security_grid',
        'base_xml_rename',
        'disable_install_from_website',
        'ir_attachment_access_token_portal',
        'ir_attachment_name_autocomplete',
        'mail_activity_not_deleted',
        'mail_follower_picker',
        'mail_message_from_author',
        'mail_notification_no_footer',
        'mail_recipient_unchecked',
        'note_no_default_stage',
        'private_data_group',
        'queue_job_auto_requeue',
        'super_calendar',
        'url_link_type',
        'web_email_field_new_tab',
    ],
    'installable': True,
}
