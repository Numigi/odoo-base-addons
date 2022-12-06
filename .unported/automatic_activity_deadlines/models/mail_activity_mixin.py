# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import models


class MailActivityMixin(models.AbstractModel):
    _inherit = "mail.activity.mixin"

    def activity_schedule(
        self, act_type_xmlid="", date_deadline=None, summary="", note="", **act_values
    ):
        res = super().activity_schedule(
            act_type_xmlid, date_deadline, summary, note, **act_values
        )
        if date_deadline:
            return res
        for rec in res.filtered(
            lambda r: r.activity_type_id and r.activity_type_id.delay_count
        ):
            activity_type = rec.activity_type_id
            date_deadline = rec.date_deadline + relativedelta(
                **{activity_type.delay_unit: activity_type.delay_count}
            )
            rec.date_deadline = date_deadline
        return res
