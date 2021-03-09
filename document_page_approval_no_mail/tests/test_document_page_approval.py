# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import SavepointCase


class TestDocumentPageApproval(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.page = cls.env["document.page"].create(
            {"name": "Some Page", "approval_required": True, "content": "Some Content"}
        )

        cls.approval_group = cls.env.ref("document_page_approval.group_document_approver_user")
        cls.user = cls.env.user
        cls.user.groups_id -= cls.approval_group

        cls.internal_note = cls.env.ref("mail.mt_note")

    def test_approval_message(self):
        self.page.content = "New Content"

        history = self._get_last_history()
        message = self._get_last_message(history)
        assert self._is_internal_note(message)

    def test_approved_message(self):
        self.page.content = "New Content"

        history = self._get_last_history()

        self.user.groups_id |= self.approval_group
        history.action_approve()

        message = self._get_last_message(history)
        assert self._is_internal_note(message)

    def test_cancel_message(self):
        self.page.content = "New Content"

        history = self._get_last_history()
        history.action_cancel()

        message = self._get_last_message(history)
        assert self._is_internal_note(message)

    def _is_internal_note(self, message):
        return (
            message.subtype_id == self.internal_note
            and message.message_type == "notification"
        )

    def _get_last_message(self, record):
        return record.message_ids.sorted("id")[-1]

    def _get_last_history(self):
        return self.env["document.page.history"].search(
            [("page_id", "=", self.page.id)], order="id desc", limit=1
        )
