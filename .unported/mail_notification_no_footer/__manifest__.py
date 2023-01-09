# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Mail Notification No Footer',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Remove the footer from the notification templates',
    'depends': [
        'mail',
    ],
    'data': [
        'views/notification_templates.xml',
    ],
    'installable': True,
}
