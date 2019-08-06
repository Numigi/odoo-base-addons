# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data
from odoo import models
from odoo.exceptions import AccessError
from odoo.osv.expression import AND
from odoo.tests import SavepointCase
from .common import mock_odoo_request
from ..controllers.main import DataSetWithExtendedSecurity


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
        for partner in self:
            if partner.employee:
                raise AccessError(EMPLOYEE_ACCESS_MESSAGE)

    def check_extended_security_read(self):
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_READ_MESSAGE)

    def check_extended_security_write(self):
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_WRITE_MESSAGE)

    def check_extended_security_create(self):
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_CREATE_MESSAGE)

    def check_extended_security_unlink(self):
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_UNLINK_MESSAGE)


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

    def setUp(self):
        super().setUp()
        self.controller = DataSetWithExtendedSecurity()

    def _search(self, domain):
        with mock_odoo_request(self.env):
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
        with mock_odoo_request(self.env):
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
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'search_count', [domain])

    def test_search_count_with_empty_domain(self):
        count = self._search_count([])
        assert count == self.customer_count

    def test_search_count_with_supplier_domain(self):
        count = self._search_count([('supplier', '=', True)])
        assert count == self.supplier_customer_count

    def _search_read(self, domain, use_search_read_route):
        with mock_odoo_request(self.env):
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
        with mock_odoo_request(self.env):
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

    def _name_get(self, records):
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'name_get', [records.ids])

    def test_on_name_get_with_employee__access_error_raised(self):
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._name_get(self.employee)

    def test_on_name_get_with_non_customer__access_error_raised(self):
        with pytest.raises(AccessError, match=NON_CUSTOMER_READ_MESSAGE):
            self._name_get(self.supplier)

    def test_on_name_get_with_customer__access_error_not_raised(self):
        self._name_get(self.customer | self.supplier_customer)

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
