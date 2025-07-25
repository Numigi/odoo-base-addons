# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Auditlog Binding Queue Job',
    'version': '14.0.1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Other',
    'summary': 'Hide logs in the auditlog module if the requests come from a queue job.',
    'depends': [
        'auditlog',
        'queue_job',
    ],
    'installable': True,
}
