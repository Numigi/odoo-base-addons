# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Base Extended Security',
    'version': "14.0.1.0.0",
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Securize access to records',
    'depends': [
        'web', 'test_http_request'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/extended_security_rule.xml',
    ],
    'installable': True,
}
