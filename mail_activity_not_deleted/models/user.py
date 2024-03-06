# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from collections import defaultdict

from odoo import api, fields, models, modules


class User(models.Model):

    _inherit = 'res.users'

    @api.model
    def systray_get_activities(self):
        """Prevent inactive activities from appearing in the main Odoo navbar.

        This method is a copy from the method defined at:
        odoo/addons/mail/models/res_users.py

        Only the active filter was added in the sql query.
        """
        query = """SELECT array_agg(res_id) as res_ids, m.id, count(*),
                    CASE
                        WHEN %(today)s::date - act.date_deadline::date = 0 Then 'today'
                        WHEN %(today)s::date - act.date_deadline::date > 0 Then 'overdue'
                        WHEN %(today)s::date - act.date_deadline::date < 0 Then 'planned'
                    END AS states
                FROM mail_activity AS act
                JOIN ir_model AS m ON act.res_model_id = m.id
                WHERE user_id = %(user_id)s
                AND act.active
                GROUP BY m.id, states;
                """
        self.env.cr.execute(
            query,
            {
                "today": fields.Date.context_today(self),
                "user_id": self.env.uid,
            },
        )
        activity_data = self.env.cr.dictfetchall()
        records_by_state_by_model = defaultdict(
            lambda: {"today": set(), "overdue": set(), "planned": set(), "all": set()}
        )
        for data in activity_data:
            records_by_state_by_model[data["id"]][data["states"]] = set(data["res_ids"])
            records_by_state_by_model[data["id"]]["all"] = records_by_state_by_model[
                data["id"]
            ]["all"] | set(data["res_ids"])
        user_activities = {}
        for model_id in records_by_state_by_model:
            model_dic = records_by_state_by_model[model_id]
            model = (
                self.env["ir.model"]
                .browse(model_id)
                .with_prefetch(tuple(records_by_state_by_model.keys()))
            )
            allowed_records = self.env[model.model].search(
                [("id", "in", tuple(model_dic["all"]))]
            )
            if not allowed_records:
                continue
            module = self.env[model.model]._original_module
            icon = module and modules.module.get_module_icon(module)
            today = len(model_dic["today"] & set(allowed_records.ids))
            overdue = len(model_dic["overdue"] & set(allowed_records.ids))
            user_activities[model.model] = {
                "name": model.name,
                "model": model.model,
                "type": "activity",
                "icon": icon,
                "total_count": today + overdue,
                "today_count": today,
                "overdue_count": overdue,
                "planned_count": len(model_dic["planned"] & set(allowed_records.ids)),
                "actions": [
                    {
                        "icon": "fa-clock-o",
                        "name": "Summary",
                    }
                ],
            }
        return list(user_activities.values())
