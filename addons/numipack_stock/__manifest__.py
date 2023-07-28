# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Numipack Stock',
    'version': '1.0.1',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Functional dependencies for all Odoo instances using the inventory.',
    'depends': [
        'numipack',

        # numigi/odoo-stock-addons
        'stock_move_origin_link',
        'stock_picking_show_address',
        'stock_account_visibility',
    ],
    'data': [
        'data/auditlog_rule.xml',
        'security/extended_security_rule.xml',
    ],
    'installable': True,
}
