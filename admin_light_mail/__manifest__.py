# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Admin Light Email',
    'version': '14.0.1.0.2',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Add email management to the Admin Light application.',
    'depends': [
        'admin_light_base',
        'fetchmail',
        'mail'
    ],
    'data': [
        'views/menu_item.xml',
        'views/mail_message_views.xml',
        'views/mail_message_subtype_views.xml',
        'views/mail_server_views.xml',
        'views/mail_template_views.xml',
        'views/mail_activity_type_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
