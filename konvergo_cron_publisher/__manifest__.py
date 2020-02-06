# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Konvergo Cron Publicher',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Disable the cron notifying odoo',
    'depends': [
        'mail',  # TA#16530
    ],
    'data': [
        'data/ir_cron_data.xml',
    ],
    'installable': True,
}
