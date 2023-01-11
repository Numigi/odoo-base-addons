# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
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
from ..controllers.crud import DataSetWithExtendedSecurity


class TestControllers(ControllerCase):

    def setUp(self):
        super().setUp()
        self.controller = DataSetWithExtendedSecurity()

    def _read(self, records):
        with mock_odoo_request(self.env):
            return self.controller.call(
                'res.partner', 'read',
                [records.ids, ['name', 'customer_rank', 'supplier_rank']]
            )

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

    def test_on_write__if_not_authorized_after_write__access_error_raised(self):
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._write(self.customer, {'employee': True})

    def test_on_write_with_customer__access_error_not_raised(self):
        self._write(self.customer | self.supplier_customer, {'name': 'My Customer'})

    def _create(self, values):
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'create', [values])

    def test_on_create_with_employee__access_error_raised(self):
        values = [{
            'name': 'My Employee',
            'supplier_rank': 1,
            'customer_rank': 1,
            'employee': True,
        }]
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._create(values)

    def test_on_create_with_non_customer__access_error_raised(self):
        values = [{
            'name': 'My Supplier',
            'customer_rank': 0,
            'supplier_rank': 1,
        }]
        with pytest.raises(AccessError, match=NON_CUSTOMER_CREATE_MESSAGE):
            self._create(values)

    def test_on_create_with_customer__access_error_not_raised(self):
        values = [
            {
                'name': 'My Customer',
                'customer_rank': 1,
                'supplier_rank': 0,
            },
            {
                'name': 'My Supplier Customer',
                'customer_rank': 1,
                'supplier_rank': 1,
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

    def _x2many_unlink(self, parent, child):
        self._write(parent, {'child_ids': [(2, child.id)]})

    def test_on_x2many_unlink_with_employee__access_error_raised(self):
        self.customer.child_ids |= self.employee
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._x2many_unlink(self.customer, self.employee)

    def test_on_x2many_unlink_with_non_customer__access_error_raised(self):
        self.customer.child_ids |= self.supplier
        with pytest.raises(AccessError, match=NON_CUSTOMER_UNLINK_MESSAGE):
            self._x2many_unlink(self.customer, self.supplier)

    def test_on_x2many_unlink_with_customer__access_error_not_raised(self):
        self.customer.child_ids |= self.supplier_customer
        self._x2many_unlink(self.customer, self.supplier_customer)

    def _x2many_write(self, parent, child):
        vals = {'name': 'Some Value'}
        self._write(parent, {'child_ids': [(1, child.id, vals)]})

    def test_on_x2many_write_with_employee__access_error_raised(self):
        self.customer.child_ids |= self.employee
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._x2many_write(self.customer, self.employee)

    def test_on_x2many_write_with_non_customer__access_error_raised(self):
        self.customer.child_ids |= self.supplier
        with pytest.raises(AccessError, match=NON_CUSTOMER_WRITE_MESSAGE):
            self._x2many_write(self.customer, self.supplier)

    def test_on_x2many_write_with_customer__access_error_not_raised(self):
        self.customer.child_ids |= self.supplier_customer
        self._x2many_write(self.customer, self.supplier_customer)

    def _x2many_create(self, parent, vals):
        self._write(parent, {'child_ids': [(0, 0, vals)]})

    # def test_on_x2many_create_with_employee__access_error_raised(self):
    #     with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
    #         self._x2many_create(self.customer, {
    #             'name': 'Some Contact',
    #             'customer_rank': 1,
    #             'supplier_rank': 1,
    #         })

    def test_on_x2many_create_with_non_customer__access_error_raised(self):
        with pytest.raises(AccessError, match=NON_CUSTOMER_WRITE_MESSAGE):
            self._x2many_create(self.customer, {
                'name': 'Some Contact',
                'customer_rank': 0,
            })

    def test_on_x2many_create_with_customer__access_error_not_raised(self):
        self._x2many_create(self.customer, {
            'name': 'Some Contact',
            'customer_rank': 1,
        })

    def _name_create(self, name):
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'name_create', [name])

    def _set_default_value(self, field, value):
        self.env['ir.default'].set('res.partner', field, value, user_id=self.env.uid)

    def test_on_name_create_with_customer__access_error_not_raised(self):
        self._set_default_value('customer_rank', 1)
        self._name_create('My Partner')

    def test_on_name_create_with_non_customer__access_error_raised(self):
        self._set_default_value('customer_rank', 0)
        with pytest.raises(AccessError, match=NON_CUSTOMER_CREATE_MESSAGE):
            self._name_create('My Partner')

    def test_on_many2many_tags_read__access_error_not_raised(self):
        fields = ['display_name', 'color']
        self._read_many2many_tags(self.employee, fields)

    def test_on_many2many_tags_read__with_all_fields_requested(self):
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._read_many2many_tags(self.employee, None)

    def _read_many2many_tags(self, records, fields):
        with mock_odoo_request(self.env):
            return self.controller.call('res.partner', 'read', [records.ids, fields])

    def _call_button(self, records, action_name):
        with mock_odoo_request(self.env):
            return self.controller.call_button('res.partner', action_name, [records.ids], {})

    def test_toggle_active_with_employee__access_error_raised(self):
        with pytest.raises(AccessError, match=EMPLOYEE_ACCESS_MESSAGE):
            self._call_button(self.employee, 'toggle_active')

    def test_toggle_active_with_customer__access_error_not_raised(self):
        self._call_button(self.customer, 'toggle_active')
