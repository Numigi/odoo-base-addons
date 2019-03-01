# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Mail Activity List',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Deactivate terminated activities instead of deleting.',
    'depends': [
        'crm',
        'mail_activity_not_deleted',
    ],
    'data': [
        'views/activity.xml',
    ],
    'installable': True,
}
