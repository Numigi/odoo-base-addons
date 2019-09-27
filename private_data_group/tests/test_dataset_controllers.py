# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from ddt import ddt, data, unpack
from odoo.addons.test_http_request.common import mock_odoo_request
from odoo.exceptions import AccessError, ValidationError
from odoo.tests.common import TransactionCase
from ..controllers.dataset import DataSetWithPrivateFields


@ddt
class TestControllers(TransactionCase):

    def setUp(self):
        super().setUp()
        self.user = self.env['res.users'].create({
            'name': 'Employee',
            'email': 'test@example.com',
            'login': 'test@example.com',
        })

        self.employee = self.env['hr.employee'].create({
            'name': 'Employee',
            'sinid': '123 456 789',
            'user_id': self.user.id,
        })
        self.fields = ('name', 'sinid')
        self.domain = [('id', '=', self.employee.id)]

        self.controller = DataSetWithPrivateFields()

    def test_private_field_removed_from_read_request(self):
        with mock_odoo_request(self.env):
            result = self.controller.call('hr.employee', 'read', [self.employee.ids, self.fields])
            assert 'name' in result[0]
            assert 'sinid' not in result[0]

    def _search_read(
        self, domain, fields, use_search_read_route=False, use_kwargs=False, order=None
    ):
        offset = 0
        limit = None
        with mock_odoo_request(self.env):
            if use_search_read_route:
                result = self.controller.search_read(
                    'hr.employee', domain=domain, fields=fields, sort=order,
                    offset=offset, limit=limit)
                return result['records']
            elif use_kwargs:
                self.controller.call_kw('hr.employee', 'search_read', [], {
                    'domain': domain, 'fields': fields,
                    'offset': offset, 'limit': limit, 'order': order,
                })
            else:
                return self.controller.call(
                    'hr.employee', 'search_read', [domain, fields, offset, limit, order])

    @data(True, False)
    def test_private_field_removed_from_search_result(self, use_search_read_route):
        with mock_odoo_request(self.env):
            result = self._search_read(self.domain, self.fields, use_search_read_route)
            assert 'name' in result[0]
            assert 'sinid' not in result[0]

    @data(
        (True, False),
        (False, True),
        (False, False),
    )
    @unpack
    def test_if_private_field_used_to_order_search_read__raise_error(
        self, use_search_read_route, use_kwargs
    ):
        with mock_odoo_request(self.env):
            with pytest.raises(AccessError):
                self._search_read(
                    self.domain, self.fields, use_search_read_route, use_kwargs, order='sinid')

    @data(True, False)
    def test_if_private_field_used_in_search_read_domain__raise_error(self, use_search_read_route):
        with mock_odoo_request(self.env):
            with pytest.raises(AccessError):
                self._search_read([('sinid', '!=', False)], self.fields, use_search_read_route)

    def _read_group(self, domain, fields, groupby, order=None, use_kwargs=False):
        offset = 0
        limit = None
        with mock_odoo_request(self.env):
            if use_kwargs:
                args = []
                kwargs = {
                    'domain': domain, 'fields': fields, 'groupby': groupby,
                    'orderby': order, 'limit': limit, 'offset': offset,
                }
            else:
                args = [domain, fields, groupby, limit, offset, order]
                kwargs = {}

            return self.controller.call_kw('hr.employee', 'read_group', args, kwargs)

    def test_private_field_not_in_read_group_result(self):
        with mock_odoo_request(self.env):
            result = self._read_group(self.domain, self.fields, ['name'], use_kwargs=True)
            assert 'name' in result[0]
            assert 'sinid' not in result[0]

    @data(
        (True, ['name', 'sinid']),
        (True, 'sinid'),
        (False, ['name', 'sinid']),
        (False, 'sinid'),
    )
    @unpack
    def test_if_private_field_used_to_group__raise_error(self, use_kwargs, groupby):
        with mock_odoo_request(self.env):
            with pytest.raises(AccessError):
                self._read_group(self.domain, self.fields, groupby, use_kwargs=use_kwargs)

    @data(
        (True, 'sinid'),
        (True, 'name,sinid desc'),
        (False, 'sinid'),
        (False, 'name,sinid desc'),
    )
    @unpack
    def test_if_private_field_used_to_order_read_group__raise_error(self, use_kwargs, order):
        with mock_odoo_request(self.env):
            with pytest.raises(AccessError):
                self._read_group(
                    self.domain, self.fields, groupby=['name'],
                    order=order, use_kwargs=use_kwargs)

    def _search(self, domain, use_kwargs=False, order=None, model='hr.employee'):
        offset = 0
        limit = None
        with mock_odoo_request(self.env):
            if use_kwargs:
                self.controller.call_kw(model, 'search', [], {
                    'domain': domain, 'offset': offset, 'limit': limit, 'order': order,
                })
            else:
                return self.controller.call(
                    model, 'search', [domain, offset, limit, order])

    @data(True, False)
    def test_if_private_field_used_to_order_search__raise_error(self, use_kwargs):
        with mock_odoo_request(self.env):
            with pytest.raises(AccessError):
                self._search(self.domain, order='sinid', use_kwargs=use_kwargs)

    def test_if_search_by_related_model__domain_checked_for_private_field(self):
        domain = [('employee_ids.sinid', '>', '123')]
        with mock_odoo_request(self.env):
            with pytest.raises(AccessError):
                self._search(domain, model='res.users')

    def test_if_search_with_invalid_domain__raise_validation_error(self):
        domain = [('wrong_relation_field.sinid', '>', '123')]
        with mock_odoo_request(self.env):
            with pytest.raises(ValidationError):
                self._search(domain, model='res.users')
