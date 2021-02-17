# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Helpdesk Ticket Phone',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'license': 'LGPL-3',
    'category': 'Base',
    'summary': 'Helpdesk Ticket Phone',
    'depends': [
        # Odoo
        "phone_validation",
        # OCA-helpdesk
        "helpdesk_mgmt",
    ],
    'data': [
        "views/helpdesk_ticket.xml",
    ],
    'external_dependencies': {
        'python': ['phonenumbers'],
    },
    'installable': True,
}
