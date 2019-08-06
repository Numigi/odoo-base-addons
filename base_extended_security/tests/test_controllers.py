# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data
from contextlib import contextmanager
from odoo import models
from odoo.http import request, HttpRequest, OpenERPSession
from odoo.osv.expression import AND
from odoo.tests import SavepointCase
from odoo.tools import config
from werkzeug.wrappers import Request
from werkzeug.contrib.sessions import FilesystemSessionStore
from werkzeug.test import EnvironBuilder
from ..controllers.main import DataSetWithExtendedSecurity


class ResPartner(models.Model):

    _inherit = 'res.partner'

    def get_extended_security_domain(self):
        domain = super().get_extended_security_domain()
        return AND((domain, [('customer', '=', True)]))


@ddt
class TestControllers(SavepointCase):

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

        cls.customer_count = cls.env['res.partner'].search_count([('customer', '=', True)])
        cls.supplier_customer_count = cls.env['res.partner'].search_count([
            '&', ('customer', '=', True), ('supplier', '=', True),
        ])

    def setUp(self):
        super().setUp()
        self.controller = DataSetWithExtendedSecurity()

    @contextmanager
    def mock_odoo_request(self):
        """Mock an Odoo HTTP request.

        This methods builds an HttpRequest object and adds it to
        the local stack of the application.

        The Odoo environment of the test fixture is injected to the
        request so that objects created in the fixture are available
        for controllers.
        """
        session = FilesystemSessionStore(
            config.session_dir, session_class=OpenERPSession, renew_missing=True)
        session.db = self.env.cr.dbname
        session.uid = self.env.uid
        session.context = self.env.context

        environ_builder = EnvironBuilder(method='POST', data={})
        environ = environ_builder.get_environ()
        httprequest = Request(environ)
        httprequest.session = session

        odoo_http_request = HttpRequest(httprequest)
        odoo_http_request._env = self.env
        with odoo_http_request:
            yield

    def _search(self, domain):
        with self.mock_odoo_request():
            return self.controller.call('res.partner', 'search', [domain])

    def test_search_with_empty_domain(self):
        ids = self._search([])
        assert self.customer.id in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    def test_search_with_supplier_domain(self):
        ids = self._search([('supplier', '=', True)])
        assert self.customer.id not in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    def _name_search(self, name, domain):
        with self.mock_odoo_request():
            name_get = self.controller.call('res.partner', 'name_search', [name, domain])
            return [r[0] for r in name_get]

    def test_name_search_with_empty_domain(self):
        ids = self._name_search('My Partner', [])
        assert self.customer.id in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    def test_name_search_with_supplier_domain(self):
        ids = self._name_search('My Partner', [('supplier', '=', True)])
        assert self.customer.id not in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    def _search_count(self, domain):
        with self.mock_odoo_request():
            return self.controller.call('res.partner', 'search_count', [domain])

    def test_search_count_with_empty_domain(self):
        count = self._search_count([])
        assert count == self.customer_count

    def test_search_count_with_supplier_domain(self):
        count = self._search_count([('supplier', '=', True)])
        assert count == self.supplier_customer_count

    def _search_read(self, domain, use_search_read_route):
        with self.mock_odoo_request():
            if use_search_read_route:
                result = self.controller.search_read('res.partner', fields=[], domain=domain)
                records = result['records']
            else:
                records = self.controller.call('res.partner', 'search_read', [domain, []])

            return [r['id'] for r in records]

    @data(True, False)
    def test_search_read_with_empty_domain(self, use_search_read_route):
        ids = self._search_read([], use_search_read_route)
        assert self.customer.id in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    @data(True, False)
    def test_search_read_with_supplier_domain(self, use_search_read_route):
        ids = self._search_read([('supplier', '=', True)], use_search_read_route)
        assert self.customer.id not in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    def _read_group(self, domain, fields, orderby):
        with self.mock_odoo_request():
            return self.controller.call(
                'res.partner', 'read_group', [domain, [], fields], {'orderby': orderby})

    def test_read_group_with_empty_domain(self):
        groups = self._read_group([], fields=['customer'], orderby='customer')
        assert len(groups) == 1
        assert groups[0]['customer_count'] == self.customer_count

    def test_read_group_with_supplier_domain(self):
        domain = [('supplier', '=', True)]
        groups = self._read_group(domain, fields=['customer'], orderby='customer')
        assert len(groups) == 1
        assert groups[0]['customer_count'] == self.supplier_customer_count
