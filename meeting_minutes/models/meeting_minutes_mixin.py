# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MeansCommunication(models.Model):
    _name = "means.communication"
    _description = "Means of communication"
    _order = "sequence,id"

    name = fields.Char(string="Name")
    sequence = fields.Integer(string="Sequence")


class MeetingMinutesMixin(models.AbstractModel):
    _name = "meeting.minutes.mixin"
    _description = "Meeting Minutes Base Model"

    name = fields.Char(string="Name", required=True)
    start_date = fields.Datetime(string="Start time", required=True)
    end_date = fields.Datetime(string="End time", required=True)
    mean_communication_id = fields.Many2one(
        "means.communication", string="Communication channel", required=True
    )
    partner_ids = fields.Many2many("res.partner", string="Attendees")
    planned_point = fields.Html("Planned Points")
    additional_note = fields.Html("Additional Note")
    resources = fields.Html("Resources")
    risks = fields.Html("Risks")
    agenda = fields.Html("Agenda")
    duty = fields.Html("Duties")
