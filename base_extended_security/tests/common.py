# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase


EMPLOYEE_ACCESS_MESSAGE = "You are not authorized to access employees."
NON_CUSTOMER_READ_MESSAGE = "You are not authorized to read non-customers."
NON_CUSTOMER_WRITE_MESSAGE = "You are not authorized to edit non-customers."
NON_CUSTOMER_CREATE_MESSAGE = "You are not authorized to create non-customers."
NON_CUSTOMER_UNLINK_MESSAGE = "You are not authorized to delete non-customers."


class ControllerCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env["res.partner"].create(
            {
                "name": "My Partner Customer",
                "supplier_rank": 0,
                "customer_rank": 1,
            }
        )
        cls.supplier = cls.env["res.partner"].create(
            {
                "name": "My Partner Supplier",
                "supplier_rank": 1,
                "customer_rank": 0,
            }
        )
        cls.supplier_customer = cls.env["res.partner"].create(
            {
                "name": "My Partner Customer Supplier",
                "supplier_rank": 1,
                "customer_rank": 1,
            }
        )
        cls.employee = cls.env["res.partner"].create(
            {
                "name": "My Partner Customer Supplier",
                "supplier_rank": 1,
                "customer_rank": 1,
                "employee": True,
            }
        )

        cls.customer_count = cls.env["res.partner"].search_count(
            [("customer_rank", ">", 0)]
        )
        cls.supplier_customer_count = cls.env["res.partner"].search_count(
            [
                "&",
                ("customer_rank", ">", 0),
                ("supplier_rank", ">", 0),
            ]
        )
