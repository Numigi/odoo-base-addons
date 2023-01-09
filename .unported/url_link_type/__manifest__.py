# © 2019 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'URL Link Types',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Recording',
    'summary': 'Add types of URL links',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/url_link_type.xml',
    ],
    'installable': True,
}
