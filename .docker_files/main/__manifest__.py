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
        'ir_attachment_access_token_portal',
        'ir_attachment_name_autocomplete',
        'mail_activity_list',  # TA#8714
        'mail_activity_not_deleted',
        'mail_recipient_unchecked',
    ],
    'installable': True,
}
