# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    event_allowed_ceu = fields.Text(
        "Continuing Education Units (CEU)"
    )
