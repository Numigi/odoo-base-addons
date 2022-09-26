# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class IrAttachmentURLTestCase(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.user_demo = self.browse_ref("base.user_demo")
        self.unprivileged_user = self.env["res.users"].create(
            {
                "name": "unprivileged test user",
                "login": "test",
                "groups_id": [
                    (
                        6,
                        0,
                        [
                            self.env.ref("base.group_user").id,
                            self.env.ref("base.group_partner_manager").id,
                        ],
                    )
                ],
            }
        )
        self.partner = self.env.ref("base.res_partner_12")
        self.attachment = self.env["ir.attachment"]

    def test_create_url_attachment(self):
        vals = {
            "name": "Test URL",
            "res_model": "res.partner",
            "res_id": self.partner.id,
            "type": 'url',
            "url": 'https://github.com/Numigi/',
        }
        attachment = self.attachment.sudo(self.unprivileged_user).create(vals)
        self.assertEquals(attachment.name, "Test URL")
        vals["name"] = "Test URL 2"
        attachment = self.attachment.sudo(self.user_demo).create(vals)
        self.assertEquals(attachment.name, "Test URL 2")
