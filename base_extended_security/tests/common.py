
from contextlib import contextmanager
from odoo import models
from odoo.api import Environment
from odoo.exceptions import AccessError
from odoo.http import HttpRequest, OpenERPSession
from odoo.osv.expression import AND
from odoo.tests.common import SavepointCase
from odoo.tools import config
from werkzeug.contrib.sessions import FilesystemSessionStore
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request


EMPLOYEE_ACCESS_MESSAGE = 'You are not authorized to access employees.'
NON_CUSTOMER_READ_MESSAGE = 'You are not authorized to read non-customers.'
NON_CUSTOMER_WRITE_MESSAGE = 'You are not authorized to edit non-customers.'
NON_CUSTOMER_CREATE_MESSAGE = 'You are not authorized to create non-customers.'
NON_CUSTOMER_UNLINK_MESSAGE = 'You are not authorized to delete non-customers.'


class ResPartner(models.Model):

    _inherit = 'res.partner'

    def get_extended_security_domain(self):
        domain = super().get_extended_security_domain()
        return AND((domain, [('customer', '=', True)]))

    def check_extended_security_all(self):
        super().check_extended_security_all()
        for partner in self:
            if partner.employee:
                raise AccessError(EMPLOYEE_ACCESS_MESSAGE)

    def check_extended_security_read(self):
        super().check_extended_security_read()
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_READ_MESSAGE)

    def check_extended_security_write(self):
        super().check_extended_security_write()
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_WRITE_MESSAGE)

    def check_extended_security_create(self):
        super().check_extended_security_create()
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_CREATE_MESSAGE)

    def check_extended_security_unlink(self):
        super().check_extended_security_unlink()
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_UNLINK_MESSAGE)


@contextmanager
def mock_odoo_request(env: Environment):
    """Mock an Odoo HTTP request.

    This methods builds an HttpRequest object and adds it to
    the local stack of the application.

    The Odoo environment of the test fixture is injected to the
    request so that objects created in the fixture are available
    for controllers.
    """
    session = FilesystemSessionStore(
        config.session_dir, session_class=OpenERPSession, renew_missing=True)
    session.db = env.cr.dbname
    session.uid = env.uid
    session.context = env.context

    environ_builder = EnvironBuilder(method='POST', data={})
    environ = environ_builder.get_environ()
    httprequest = Request(environ)
    httprequest.session = session

    odoo_http_request = HttpRequest(httprequest)
    odoo_http_request._env = env
    with odoo_http_request:
        yield


class ControllerCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env['res.partner'].create({
            'name': 'My Partner Customer',
            'supplier': False,
            'customer': True,
        })
        cls.supplier = cls.env['res.partner'].create({
            'name': 'My Partner Supplier',
            'supplier': True,
            'customer': False,
        })
        cls.supplier_customer = cls.env['res.partner'].create({
            'name': 'My Partner Customer Supplier',
            'supplier': True,
            'customer': True,
        })
        cls.employee = cls.env['res.partner'].create({
            'name': 'My Partner Customer Supplier',
            'supplier': True,
            'customer': True,
            'employee': True,
        })

        cls.customer_count = cls.env['res.partner'].search_count([('customer', '=', True)])
        cls.supplier_customer_count = cls.env['res.partner'].search_count([
            '&', ('customer', '=', True), ('supplier', '=', True),
        ])
