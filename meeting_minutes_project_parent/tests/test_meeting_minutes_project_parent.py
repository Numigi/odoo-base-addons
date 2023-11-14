# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests.common import SavepointCase


class TestMeetingMinutesProjectParent(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_1 = cls.env["project.project"].create({"name": "Project 1"})
        cls.project_2 = cls.env["project.project"].create({"name": "Project 2"})

        cls.task_1 = cls.env["project.task"].create(
            {
                "project_id": cls.project_1.id,
                "name": "Task 1",
            }
        )

        cls.task_2 = cls.env["project.task"].create(
            {
                "project_id": cls.project_1.id,
                "name": "Task 2",
            }
        )
        cls.task_3 = cls.env["project.task"].create(
            {
                "project_id": cls.project_2.id,
                "name": "Task 3",
            }
        )

    def test_project_child_meeting_minutes(self):
        self.task_1.open_meeting_minutes()
        self.task_2.open_meeting_minutes()
        self.project_1.write({"parent_id": self.project_2.id})
        self.project_2._compute_meeting_minutes_project()
        assert 2 == self.project_2.meeting_minutes_project_count
        self.task_3.open_meeting_minutes()
        self.project_2._compute_meeting_minutes_project()
        assert 3 == self.project_2.meeting_minutes_project_count
