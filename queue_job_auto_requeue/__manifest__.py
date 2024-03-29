# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Queue Job Auto Requeue',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Automatically reset queue jobs to pending after a given time.',
    'depends': [
        'queue_job',
    ],
    'data': [
        'data/ir_cron.xml',
    ],
    'installable': True,
    'auto_install': True,
}
