# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta
from odoo import models


class MailActivityMixin(models.AbstractModel):
    _inherit = "mail.activity.mixin"

    def activity_schedule(
        self, act_type_xmlid="", date_deadline=None, summary="", note="", **act_values
    ):
        activities = super().activity_schedule(
            act_type_xmlid, date_deadline, summary, note, **act_values
        )

        if activities and not date_deadline:
            _apply_automatic_deadline(activities)

        return activities


def _apply_automatic_deadline(activities):
    for activity in activities.filtered(_should_apply_automatic_deadline):
        activity.date_deadline = _compute_automatic_deadline(activity)


def _should_apply_automatic_deadline(activity):
    return activity.activity_type_id.delay_count


def _compute_automatic_deadline(activity):
    activity_type = activity.activity_type_id
    return activity.date_deadline + relativedelta(
        **{activity_type.delay_unit: activity_type.delay_count}
    )
