# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.test_http_request.common import mock_odoo_request
from odoo.tests.common import TransactionCase
from ..controllers.portal import PortalChatterWithAttachments


class TestControllers(TransactionCase):
    def setUp(self):
        super().setUp()
        self.controller = PortalChatterWithAttachments()
        self.task = self.env["project.task"].create({"name": "My Task"})
        self.res_model = "project.task"
        self.res_id = self.task.id
        self.message = "Hello"
        self.initial_message_count = self._get_message_count()
        self.headers = {
            "Referer": "localhost/my/task",
            "Content-Type": "multipart/form-data",
        }

    def test_portal_chatter_post(self):
        with mock_odoo_request(self.env, headers=self.headers):
            self.controller.portal_chatter_post(
                self.res_model, self.res_id, self.message
            )

        assert self._get_message_count() == self.initial_message_count + 1

    def _get_message_count(self):
        return len(self.task.message_ids)
