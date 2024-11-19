# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError


class TestMailTemplateAccess(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        ref = cls.env.ref
        cls.user1 = cls.env["res.users"].create(
            {
                "name": "User 1",
                "login": "user1",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            ref("base.group_user").id,
                            ref("admin_light_mail.group_email_template").id,
                        ],
                    )
                ],
            }
        )
        cls.user2 = cls.env["res.users"].create(
            {
                "name": "User 2",
                "login": "user2",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            ref("base.group_user").id,
                            ref("admin_light_mail.group_email_template").id,
                        ],
                    )
                ],
            }
        )
        cls.mail_template_user1 = (
            cls.env["mail.template"]
            .with_user(cls.user1)
            .create(
                {
                    "name": "User1 Template",
                    "subject": "Template by User1",
                    "email_from": "user1@example.com",
                }
            )
        )

    def test_user_own_record_access(self):
        self.mail_template_user1.with_user(self.user1).write(
            {"subject": "Updated by User1"}
        )
        self.assertEqual(self.mail_template_user1.subject, "Updated by User1")
        self.mail_template_user1.with_user(self.user1).unlink()
        self.assertFalse(
            self.env["mail.template"].search([("id", "=", self.mail_template_user1.id)])
        )

    def test_other_user_access_error(self):
        self.mail_template_user1 = (
            self.env["mail.template"]
            .with_user(self.user1)
            .create(
                {
                    "name": "User1 Template",
                    "subject": "Template by User1",
                    "email_from": "user1@example.com",
                }
            )
        )
        with self.assertRaises(AccessError):
            self.mail_template_user1.with_user(self.user2).write(
                {"subject": "Unauthorized Update by User2"}
            )
        with self.assertRaises(AccessError):
            self.mail_template_user1.with_user(self.user2).unlink()
