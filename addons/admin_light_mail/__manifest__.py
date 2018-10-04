# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Admin Light Email',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Add email management to the Admin Light application.',
    'depends': [
        'admin_light_base',
        'fetchmail',
    ],
    'data': [
        'common.xml',
        'email_and_messages.xml',
        'mail_template.xml',
        'mail_server.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
