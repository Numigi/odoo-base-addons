# © 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# © 2012 Domsense srl (<http://www.domsense.com>)
# © 2015 Anubía, soluciones en la nube,SL (http://www.anubia.es)
#                Alejandro Santana <alejandrosantana@anubia.es>
# © 2015 Savoir-faire Linux <http://www.savoirfairelinux.com>)
#                Agathe Mollé <agathe.molle@savoirfairelinux.com>
# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class SuperCalendarConfigurator(models.Model):

    _name = 'super.calendar.configurator'
    _description = 'Super Calendar Configurator'

    name = fields.Char(
        string='Name',
    )
    line_ids = fields.One2many(
        comodel_name='super.calendar.configurator.line',
        inverse_name='configurator_id',
        string='Lines',
    )

    @api.model
    def generate_calendar_records(self):
        """Generate calendar records for all super calendars.

        This method is called by the cron.
        """
        for configurator in self.search([]):
            configurator.action_generate_calendar_records()
        return True

    @api.multi
    def action_generate_calendar_records(self):
        """Generate the super calendar for one configurator."""
        for line in self.mapped('line_ids'):
            line.generate_calendar_records()
        return True
