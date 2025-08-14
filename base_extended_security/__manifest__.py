# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Base Extended Security',
    'version': '1.2.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Securize access to records',
    'depends': [
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/extended_security_rule.xml',
    ],
    'installable': True,
}
