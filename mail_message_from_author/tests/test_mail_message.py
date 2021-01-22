# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestMailMessage(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_demo = cls.env.ref("base.user_demo")
        cls.user_demo.groups_id |= cls.env.ref("sales_team.group_sale_manager")

        cls.author_email = "john.doe@example.com"
        cls.customer = cls.env["res.partner"].create(
            {"name": "My Customer"},
        )
        cls.author = cls.env["res.partner"].create(
            {"name": "Message Author", "email": cls.author_email}
        )
        cls.product = cls.env["product.product"].create({"name": "My Product"})
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.customer.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": "/",
                            "product_id": cls.product.id,
                            "product_uom_id": cls.product.uom_id.id,
                            "product_uom_qty": 1,
                        },
                    )
                ],
            }
        )
        cls.body = "A message from my customer"

    def test_if_from_odoobot__author_propagated(self):
        self.order.sudo().message_post(body=self.body, author_id=self.author.id)
        message = self.order.message_ids.filtered(lambda m: self.body in m.body)
        assert self.author_email in message.email_from

    def test_if_not_from_odoobot__author_not_propagated(self):
        self.order.sudo(self.user_demo).message_post(body=self.body, author_id=self.author.id)
        message = self.order.message_ids.filtered(lambda m: self.body in m.body)
        assert self.author_email not in message.email_from
