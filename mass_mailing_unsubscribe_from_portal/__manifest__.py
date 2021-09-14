# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Mass Mailing Unsubscribe From Portal',
    'version': '1.0.0',
    'author': 'Numigi',
    'maintainer': 'Numigi',
    'website': 'https://www.numigi.com',
    'license': 'LGPL-3',
    'category': 'Base',
    'summary': 'Allow to unsubscribe from mass mailing lists from the portal',
    'depends': [
         'portal',
         'mass_mailing',
     ],
    'data': [
         'views/portal.xml',
    ],
    'installable': True,
}
