# © 2020 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'NumiKube',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Extra Tools',
    'summary': 'Modules required for the Numigi Kubernetes Infrastructure',
    'depends': [
        'numikube_attachment_minio',
        'numikube_database_backup',
        'session_redis',
    ],
    'installable': True,
}
