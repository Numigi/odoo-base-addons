# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class BaseWithUnlinkPropagatedToCalendarEvents(models.AbstractModel):
    """When unlinking a record, related calendar envents are deleted."""

    _inherit = 'base'

    @api.multi
    def unlink(self):
        if self._name != 'super.calendar':
            self.env['super.calendar'].search([
                ('res_id', 'in', self.mapped(lambda r: '{},{}'.format(r._name, r.id))),
            ]).unlink()
        return super().unlink()
