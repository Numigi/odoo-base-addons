# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests.common import SavepointCase


class TestAutomaticActivityDeadlines(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["res.users"].create({"name": "manager", "login": "manager"})
        cls.partner = cls.user.partner_id
        cls.today = fields.Date.context_today(cls.partner)
        cls.activity_type_no_delay = cls.env["mail.activity.type"].create(
            {
                "name": "No delay",
                "delay_count": 0,
                "time_type": "other",
                "allocation_type": "no",
                "validity_start": False,
            }
        )
        cls.activity_type_5_days_delay = cls.activity_type_no_delay.copy(
            default={
                "name": "Five days delay",
                "delay_count": 5,
                "delay_unit": "days",
                "delay_from": "current_date",
            }
        )
        cls.activity_type_2_months_delay = cls.activity_type_no_delay.copy(
            default={
                "name": "Two months delay",
                "delay_count": 2,
                "delay_unit": "months",
                "delay_from": "previous_activity",
            }
        )

    def test_no_delay(self):
        self._create_activity(self.activity_type_no_delay)
        activity = self._get_activity()
        self.assertEqual(activity.date_deadline, self.today)

    def test_5_days_delay(self):
        self._create_activity(self.activity_type_5_days_delay)
        activity = self._get_activity()
        self.assertEqual(activity.date_deadline, self.today + relativedelta(days=5))

    def test_2_months_delay(self):
        self._create_activity(self.activity_type_2_months_delay)
        activity = self._get_activity()
        self.assertEqual(activity.date_deadline, self.today + relativedelta(months=2))

    def test_auto_scheduled_next_activity(self):
        self.activity_type_2_months_delay.write(
            {
                "force_next": True,
                "default_next_type_id": self.activity_type_5_days_delay.id,
            }
        )
        self._create_activity(self.activity_type_2_months_delay)
        activity = self._get_activity()
        activity.action_done_schedule_next()
        next_activity = self._get_activity()
        self.assertEqual(
            next_activity.date_deadline, self.today + relativedelta(days=5)
        )

    def test_auto_scheduled_next_activity_from_previous_activity(self):
        self.activity_type_5_days_delay.write(
            {
                "force_next": True,
                "default_next_type_id": self.activity_type_2_months_delay.id,
            }
        )
        self._create_activity(self.activity_type_5_days_delay)
        activity = self._get_activity()
        activity.action_done_schedule_next()
        next_activity = self._get_activity()
        self.assertEqual(
            next_activity.date_deadline,
            self.today + relativedelta(days=5) + relativedelta(months=2),
        )

    def _create_activity(self, activity_type, context=None):
        if not context:
            context = {}
        self.partner.with_context(context).activity_schedule(
            user_id=self.user.id, activity_type_id=activity_type.id
        )

    def _get_activity(self):
        return self.env["mail.activity"].search(
            [("res_model", "=", "res.partner"), ("res_id", "=", self.partner.id)],
            order="id desc",
            limit=1,
        )
