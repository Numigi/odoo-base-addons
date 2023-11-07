# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectProject(models.Model):
    _inherit = "project.project"

    project_meeting_minutes_ids = fields.Many2many(
        "project.meeting.minutes",
        compute="_compute_project_meeting_minutes",
        string="Meeting minutes associated to this task",
    )
    project_meeting_minutes_count = fields.Integer(
        string="Meeting minutes",
        compute="_compute_project_meeting_minutes",
        groups="project.group_project_user",
    )
    pending_actions_ids = fields.Many2many(
        "mail.activity", string="Pending Actions", compute="_compute_pending_action_ids"
    )

    @api.multi
    def _compute_project_meeting_minutes(self):
        for project in self:
            project.project_meeting_minutes_ids = self.env[
                "project.meeting.minutes"
            ].search(
                [
                    ("project_id", "=", project.id),
                ]
            )
            project.project_meeting_minutes_count = len(
                project.project_meeting_minutes_ids
            )

    @api.multi
    def _compute_pending_action_ids(self):
        homework = self.env.ref("project_meeting_minutes.activity_homework")
        today = fields.Date.context_today(self)

        for rec in self:
            activities = self.env["mail.activity"].search(
                [("res_id", "in", rec.task_ids.ids)],
            )
            rec.pending_actions_ids = activities.filtered(
                lambda a: (
                    a.activity_type_id == homework
                    and a.res_model == "project.task"
                    and a.date_deadline < today
                )
            )
