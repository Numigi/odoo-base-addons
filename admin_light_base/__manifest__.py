# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Admin Light',
    'version': '1.0.2',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Add an admin menu with restricted functionalities.',
    'depends': ['base'],
    'data': [
        'base.xml',
        'sequence.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True
}
