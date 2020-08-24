# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Mail Enable Archive',
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
    #     'security/res_groups.xml',
    #     'security/ir.model.access.csv',
    #     'security/ir_rule.xml',
    #     'views/recording.xml',
         'views/mail_template.xml',
    ],
    # 'demo': [
    #     'demo/recording.xml',
    # ],
    # 'installable': True,
    # 'application': True,
}