# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class MeetingMinutesMixin(models.AbstractModel):
    _name = "meeting.minutes.mixin"
    _description = "Meeting Minutes Mixin"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _auto = True

    @api.model
    def default_get(self, fields):
        # super default_model='project.task' for easier use in adddons
        if (self.env.context.get("default_res_model") and
                not self.env.context.get("default_res_model_id")):
            self = self.with_context(
                default_res_model_id=self.env["ir.model"].sudo().search([
                    ("model", "=", self.env.context["default_res_model"])
                ], limit=1).id
            )

        defaults = super(MeetingMinutesMixin, self).default_get(fields)
        return defaults

    name = fields.Char(string="Name")
    active = fields.Boolean("Active", default=True)
    start_date = fields.Datetime(string="Start")
    end_date = fields.Datetime(string="End")
    meeting_channel_id = fields.Many2one(
        "meeting.channel", string="Communication channel"
    )
    partner_ids = fields.Many2many(
        "res.partner",
        string="Attendees",
        default=lambda self: self.env.user.partner_id
    )
    user_id = fields.Many2one(
        "res.users",
        "User",
        default=lambda self: self.env.user
    )
    planned_points = fields.Html("Planned Points")
    discussed_points = fields.Html("Discussed Points")
    resources = fields.Html("Resources")
    risks = fields.Html("Risks")
    duties = fields.Html("Duties")

    # linked document
    res_id = fields.Integer("Document ID")
    res_model_id = fields.Many2one("ir.model", "Document Model", ondelete="cascade")
    res_model = fields.Char(
        "Document Model Name",
        related="res_model_id.model",
        readonly=True,
        store=True
    )
