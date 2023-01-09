# © 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# © 2012 Domsense srl (<http://www.domsense.com>)
# © 2015 Anubía, soluciones en la nube,SL (http://www.anubia.es)
#                Alejandro Santana <alejandrosantana@anubia.es>
# © 2015 Savoir-faire Linux <http://www.savoirfairelinux.com>)
#                Agathe Mollé <agathe.molle@savoirfairelinux.com>
# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Super Calendar',
    'version': '1.0.0',
    'category': 'Generic Modules/Others',
    'summary': 'This module allows to create configurable calendars.',
    'author': ('Agile Business Group, '
               'Alejandro Santana, '
               'Agathe Mollé, '
               'Odoo Community Association (OCA)'),
    'website': 'https://bit.ly/numigi-com',
    'license': 'AGPL-3',
    'depends': ['calendar'],
    'data': [
        'views/super_calendar_view.xml',
        'data/cron_data.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
