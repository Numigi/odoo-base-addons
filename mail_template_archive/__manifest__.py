# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Mail Template Archive',
    'version': '1.2.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Base',
    'summary': 'A base module to enable mail archiving',
    'depends': [
         'base',
         'mail',
     ],
    'data': [
         'views/mail_template.xml',
    ],
    'installable': True,
}
