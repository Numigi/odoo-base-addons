# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MeetingChannel(models.Model):
    _name = "meeting.channel"
    _description = "Meeting Channel"
    _order = "sequence,id"

    name = fields.Char(string="Name")
    sequence = fields.Integer(string="Sequence")
