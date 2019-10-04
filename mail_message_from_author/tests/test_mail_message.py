# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestMailMessage(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer_name = "John Doe"
        cls.customer_email = "john.doe@example.com"
        cls.expected_email_from = "John Doe <john.doe@example.com>"
        cls.customer = cls.env['res.partner'].create({
            'name': cls.customer_name,
            'email': cls.customer_email,
        })
        cls.product = cls.env['product.product'].create({'name': 'My Product'})
        cls.order = cls.env['sale.order'].create({
            'partner_id': cls.customer.id,
            'order_line': [(0, 0, {
                'name': '/',
                'product_id': cls.product.id,
                'product_uom_id': cls.product.uom_id.id,
                'product_uom_qty': 1,
            })]
        })

    def test_on_message_post__author_propagated_to_email_from(self):
        message_body = "A message from my customer"
        self.order.message_post(body=message_body, author_id=self.customer.id)
        message = self.order.message_ids.filtered(lambda m: message_body in m.body)
        assert message.email_from == self.expected_email_from
