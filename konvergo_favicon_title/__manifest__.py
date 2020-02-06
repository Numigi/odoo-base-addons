# © 2020 - Today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Konvergo Favicon & title',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Setup of favicon and title for konvergo instance',
    'depends': [
        'web',  # TA#16527
    ],
    'data': [
        'views/webclient_templates.xml',
        'views/assets.xml',
    ],
    'installable': True,
}
