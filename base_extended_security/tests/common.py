# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import contextlib
from unittest.mock import MagicMock, patch
from odoo import models, api
from odoo.exceptions import AccessError
from odoo.osv.expression import AND
from odoo.tests.common import TransactionCase

EMPLOYEE_ACCESS_MESSAGE = "You are not authorized to access employees."
NON_CUSTOMER_READ_MESSAGE = "You are not authorized to read non-customers."
NON_CUSTOMER_WRITE_MESSAGE = "You are not authorized to edit non-customers."
NON_CUSTOMER_CREATE_MESSAGE = "You are not authorized to create non-customers."
NON_CUSTOMER_UNLINK_MESSAGE = "You are not authorized to delete non-customers."


class ResPartner(models.Model):
    _inherit = "res.partner"

    def get_extended_security_domain(self):
        """ Inject custom domain for security testing. """
        domain = super().get_extended_security_domain()
        return AND((domain, [("color", ">", 0)]))

    def check_extended_security_all(self):
        """ Restrict access to employee records. """
        super().check_extended_security_all()
        for partner in self:
            if partner.is_company:
                raise AccessError(EMPLOYEE_ACCESS_MESSAGE)

    def check_extended_security_read(self):
        """ Restrict read access to non-customer records. """
        super().check_extended_security_read()
        for partner in self:
            if partner.color < 1:
                raise AccessError(NON_CUSTOMER_READ_MESSAGE)

    def check_extended_security_write(self):
        """ Restrict write access to non-customer records. """
        super().check_extended_security_write()
        for partner in self:
            if partner.color < 1:
                raise AccessError(NON_CUSTOMER_WRITE_MESSAGE)

    def check_extended_security_create(self):
        """ Restrict create access to non-customer records. """
        super().check_extended_security_create()
        for partner in self:
            if partner.color < 1:
                raise AccessError(NON_CUSTOMER_CREATE_MESSAGE)

    def check_extended_security_unlink(self):
        """ Restrict unlink access to non-customer records. """
        super().check_extended_security_unlink()
        for partner in self:
            if partner.color < 1:
                raise AccessError(NON_CUSTOMER_UNLINK_MESSAGE)

    @api.model
    def get_read_access_actions(self):
        """ Allow specific action in read-only mode for testing. """
        res = super().get_read_access_actions()
        res.append("create_company")
        return res


class ControllerCase(TransactionCase):
    """ Base test class setting up the test records and the HTTP request mock. """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env["res.partner"].create({
            "name": "My Partner Customer",
            "color": 1,
            "is_company": False,
        })
        cls.supplier = cls.env["res.partner"].create({
            "name": "My Partner Supplier",
            "color": 0,
            "is_company": False,
        })
        cls.supplier_customer = cls.env["res.partner"].create({
            "name": "My Partner Customer Supplier",
            "color": 2,
            "is_company": False,
        })
        cls.employee = cls.env["res.partner"].create({
            "name": "My Employee Partner",
            "color": 1,
            "is_company": True,
        })

        cls.customer_count = cls.env["res.partner"].search_count([("color", ">", 0)])
        cls.supplier_customer_count = cls.env["res.partner"].search_count([
            "&", ("color", ">", 0), ("color", ">", 0),
        ])

    def setUp(self):
        super().setUp()
        self.mock_request = MagicMock()
        self.mock_request.env = self.env
        self.mock_request._cr = self.env.cr


@contextlib.contextmanager
def mock_request_env(env):
    """
    Context manager to inject a mock request into BOTH our module and Odoo's native modules.
    This prevents 'RuntimeError: object unbound' when calling super() in controllers.
    """
    mock_req = MagicMock()
    mock_req.env = env
    mock_req._cr = env.cr
    mock_req.session = MagicMock()

    patches = [
        patch("base_extended_security.controllers.crud.request", mock_req),
        patch("base_extended_security.controllers.search.request", mock_req),
        patch("base_extended_security.controllers.web_export.request", mock_req),
        patch("odoo.addons.web.controllers.dataset.request", mock_req),
        patch("odoo.addons.web.controllers.export.request", mock_req),
    ]

    for p in patches:
        p.start()
    try:
        yield mock_req
    finally:
        for p in patches:
            p.stop()