# © 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# © 2012 Domsense srl (<http://www.domsense.com>)
# © 2015 Anubía, soluciones en la nube,SL (http://www.anubia.es)
#                Alejandro Santana <alejandrosantana@anubia.es>
# © 2015 Savoir-faire Linux <http://www.savoirfairelinux.com>)
#                Agathe Mollé <agathe.molle@savoirfairelinux.com>
# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


def _models_get(self):
    model_obj = self.env['ir.model']
    model_list = model_obj.search([])
    return [(model.model, model.name) for model in model_list]


class SuperCalendar(models.Model):
    _name = 'super.calendar'
    _description = 'Super Calendar'

    name = fields.Char(
        string='Description',
        readonly=True,
    )
    date_start = fields.Datetime(
        string='Start date',
        readonly=True,
    )
    duration = fields.Float(
        string='Duration',
        readonly=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='User',
        readonly=True,
    )
    configurator_id = fields.Many2one(
        comodel_name='super.calendar.configurator',
        string='Configurator',
        readonly=True,
    )
    configurator_line_id = fields.Many2one(
        comodel_name='super.calendar.configurator.line',
        string='Configurator Line',
        readonly=True,
        ondelete='cascade',
    )
    res_id = fields.Reference(
        selection=_models_get,
        string='Resource',
        readonly=True,
    )
    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Model',
        readonly=True,
    )
