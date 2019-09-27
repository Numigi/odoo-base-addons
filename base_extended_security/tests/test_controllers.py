# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data, unpack
from odoo.addons.test_http_request.common import mock_odoo_request
from odoo.exceptions import AccessError
from .common import (
    ControllerCase,
    EMPLOYEE_ACCESS_MESSAGE,
    NON_CUSTOMER_READ_MESSAGE,
    NON_CUSTOMER_WRITE_MESSAGE,
    NON_CUSTOMER_CREATE_MESSAGE,
    NON_CUSTOMER_UNLINK_MESSAGE,
)
from ..controllers.main import DataSetWithExtendedSecurity


@ddt
class TestControllers(ControllerCase):

    def setUp(self):
        super().setUp()
        self.controller = DataSetWithExtendedSecurity()

    def _search(self, domain, domain_kwarg):
        with mock_odoo_request(self.env):
            args = [] if domain_kwarg else [domain]
            kwargs = {'args': domain} if domain_kwarg else {}
            return self.controller.call_kw('res.partner', 'search', args, kwargs)

    @data(True, False)
    def test_search_with_empty_domain(self, domain_kwarg):
        ids = self._search([], domain_kwarg)
        assert self.customer.id in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    @data(True, False)
    def test_search_with_supplier_domain(self, domain_kwarg):
        ids = self._search([('supplier', '=', True)], domain_kwarg)
        assert self.customer.id not in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    def _name_search(self, name, domain, name_kwarg, domain_kwarg):
        with mock_odoo_request(self.env):
            args = []
            kwargs = {}

            if name_kwarg:
                kwargs['name'] = name
            else:
                args.append(name)

            if domain_kwarg:
                kwargs['args'] = domain
            else:
                args.append(domain)

            name_get = self.controller.call_kw('res.partner', 'name_search', args, kwargs)
            return [r[0] for r in name_get]

    @data(
        (True, True),
        (False, False),
        (False, True),
    )
    @unpack
    def _test_name_search_with_empty_domain(self, name_kwarg, domain_kwarg):
        ids = self._name_search('My Partner', [], name_kwarg, domain_kwarg)
        assert self.customer.id in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    @data(
        (True, True),
        (False, False),
        (False, True),
    )
    @unpack
    def test_name_search_with_supplier_domain(self, name_kwarg, domain_kwarg):
        ids = self._name_search('My Partner', [('supplier', '=', True)], name_kwarg, domain_kwarg)
        assert self.customer.id not in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    def _search_count(self, domain, domain_kwarg):
        with mock_odoo_request(self.env):
            args = [] if domain_kwarg else [domain]
            kwargs = {'args': domain} if domain_kwarg else {}
            return self.controller.call_kw('res.partner', 'search_count', args, kwargs)

    @data(True, False)
    def test_search_count_with_empty_domain(self, domain_kwarg):
        count = self._search_count([], domain_kwarg)
        assert count == self.customer_count

    @data(True, False)
    def test_search_count_with_supplier_domain(self, domain_kwarg):
        count = self._search_count([('supplier', '=', True)], domain_kwarg)
        assert count == self.supplier_customer_count

    def _search_read(self, domain, use_search_read_route, domain_kwarg):
        with mock_odoo_request(self.env):
            if use_search_read_route:
                result = self.controller.search_read('res.partner', fields=[], domain=domain)
                records = result['records']
            elif domain_kwarg:
                records = self.controller.call('res.partner', 'search_read', [domain, []])
            else:
                records = self.controller.call_kw(
                    'res.partner', 'search_read', [], {'domain': domain})

            return [r['id'] for r in records]

    @data(
        (True, False),
        (False, False),
        (False, True),
    )
    @unpack
    def test_search_read_with_empty_domain(self, use_search_read_route, domain_kwarg):
        ids = self._search_read([], use_search_read_route, domain_kwarg)
        assert self.customer.id in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    @data(
        (True, False),
        (False, False),
        (False, True),
    )
    @unpack
    def test_search_read_with_supplier_domain(self, use_search_read_route, domain_kwarg):
        ids = self._search_read([('supplier', '=', True)], use_search_read_route, domain_kwarg)
        assert self.customer.id not in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    def _read_group(self, domain, fields, groupby, domain_kwarg):
        with mock_odoo_request(self.env):
            if domain_kwarg:
                args = []
                kwargs = {
                    'domain': domain, 'fields': fields,
                    'groupby': groupby, 'orderby': groupby
                }
            else:
                args = [domain, [], fields, groupby]
                kwargs = {'orderby': groupby}

            return self.controller.call_kw('res.partner', 'read_group', args, kwargs)

    @data(True, False)
    def test_read_group_with_empty_domain(self, domain_kwarg):
        groups = self._read_group(
            [], fields=['customer'], groupby='customer', domain_kwarg=domain_kwarg)
        assert len(groups) == 1
        assert groups[0]['customer_count'] == self.customer_count

    @data(True, False)
    def test_read_group_with_supplier_domain(self, domain_kwarg):
        domain = [('supplier', '=', True)]
        groups = self._read_group(
            domain, fields=['customer'], groupby='customer', domain_kwarg=domain_kwarg)
        assert len(groups) == 1
        assert groups[0]['customer_count'] == self.supplier_customer_count

    def _read(self, records):
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'read', [records.ids, ['name']])

    def test_on_read_with_employee__access_error_raised(self):
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._read(self.employee)

    def test_on_read_with_non_customer__access_error_raised(self):
        with pytest.raises(AccessError, match=NON_CUSTOMER_READ_MESSAGE):
            self._read(self.supplier)

    def test_on_read_with_customer__access_error_not_raised(self):
        self._read(self.customer | self.supplier_customer)

    def _write(self, records, values):
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'write', [records.ids, values])

    def test_on_write_with_employee__access_error_raised(self):
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._write(self.employee, {'name': 'My Employee'})

    def test_on_write_with_non_customer__access_error_raised(self):
        with pytest.raises(AccessError, match=NON_CUSTOMER_WRITE_MESSAGE):
            self._write(self.supplier, {'name': 'My Supplier'})

    def test_on_write_with_customer__access_error_not_raised(self):
        self._write(self.customer | self.supplier_customer, {'name': 'My Customer'})

    def _create(self, values):
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'create', [values])

    def test_on_create_with_employee__access_error_raised(self):
        values = [{
            'name': 'My Employee',
            'customer': True,
            'supplier': True,
            'employee': True,
        }]
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._create(values)

    def test_on_create_with_non_customer__access_error_raised(self):
        values = [{
            'name': 'My Supplier',
            'customer': False,
            'supplier': True,
        }]
        with pytest.raises(AccessError, match=NON_CUSTOMER_CREATE_MESSAGE):
            self._create(values)

    def test_on_create_with_customer__access_error_not_raised(self):
        values = [
            {
                'name': 'My Customer',
                'customer': True,
                'supplier': False,
            },
            {
                'name': 'My Supplier Customer',
                'customer': True,
                'supplier': True,
            }
        ]
        self._create(values)

    def _unlink(self, records):
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'unlink', [records.ids])

    def test_on_unlink_with_employee__access_error_raised(self):
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._unlink(self.employee)

    def test_on_unlink_with_non_customer__access_error_raised(self):
        with pytest.raises(AccessError, match=NON_CUSTOMER_UNLINK_MESSAGE):
            self._unlink(self.supplier)

    def test_on_unlink_with_customer__access_error_not_raised(self):
        self._unlink(self.customer | self.supplier_customer)

    def _name_create(self, name):
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'name_create', [name])

    def _set_default_value(self, field, value):
        self.env['ir.default'].set('res.partner', field, value, user_id=self.env.uid)

    def test_on_name_create_with_customer__access_error_not_raised(self):
        self._set_default_value('customer', True)
        self._name_create('My Partner')

    def test_on_name_create_with_non_customer__access_error_raised(self):
        self._set_default_value('customer', False)
        with pytest.raises(AccessError, match=NON_CUSTOMER_CREATE_MESSAGE):
            self._name_create('My Partner')

    def test_on_name_create_with_employee__access_error_not_raised(self):
        self._set_default_value('customer', True)
        self._set_default_value('customer', False)
        with pytest.raises(AccessError, match=NON_CUSTOMER_CREATE_MESSAGE):
            self._name_create('My Partner')
