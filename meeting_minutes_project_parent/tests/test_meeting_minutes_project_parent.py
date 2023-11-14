# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from datetime import timedelta
from pytz import timezone
from odoo import fields
from odoo.addons.meeting_minutes_project.tests.test_project_meeting_minutes import (
    TestMeetingMinutesProject,
)


class TestMeetingMinutesProjectParent(TestMeetingMinutesProject):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_3 = cls.env["project.project"].create({"name": "Project 3"})
        cls.task_3 = cls.env["project.task"].create(
            {
                "project_id": cls.project_3.id,
                "name": "Task 3",
            }
        )

    def test_project_child_meeting_minutes(self):
        self.task_1.open_meeting_minutes()
        self.task_2.open_meeting_minutes()
        self.project_1.write({"parent_id": self.project_3.id})
        self.project_3._compute_meeting_minutes_project()
        assert 2 == self.project_3.meeting_minutes_project_count
        self.task_3.open_meeting_minutes()
        self.project_3._compute_meeting_minutes_project()
        assert 3 == self.project_3.meeting_minutes_project_count
