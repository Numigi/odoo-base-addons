# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    event_allowed_ceu = fields.Text(
        "Continuing Education Units (CEU)"
    )
