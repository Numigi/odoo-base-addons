# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Private Data Group',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'summary': 'Add security over confidential data',
    'depends': [
        'base_extended_security',
        'hr',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir_private_field.xml',
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/ir_private_field.xml',
    ],
    'installable': True,
    'post_init_hook': 'post_init',
}
