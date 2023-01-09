# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import pytest
from ddt import ddt, data
from odoo.addons.test_http_request.common import mock_odoo_request
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase
from ..controllers.web_export import CSVControllerWithPrivateFields


@ddt
class TestWebExport(TransactionCase):

    def setUp(self):
        super().setUp()
        self.employee = self.env['hr.employee'].create({
            'name': 'My Employee',
            'sinid': '123 456 789',
        })
        self.controller = CSVControllerWithPrivateFields()

        self.env = self.env(user=self.env.ref("base.user_demo"))

    def _export(self, ids, domain, fields, model='hr.employee'):
        params = {
            'model': model,
            'ids': ids,
            'domain': domain,
            'import_compat': True,
            'fields': fields,
        }
        data_ = json.dumps(params)
        token = 'test1234'
        with mock_odoo_request(self.env):
            response = self.controller.base(data_, token)
            return response.data.decode('utf-8')

    def test_if_private_field_in_fields_to_export__raise_error(self):
        fields = [{'name': 'name'}, {'name': 'sinid'}]
        with pytest.raises(AccessError):
            self._export(ids=self.employee.ids, domain=None, fields=fields)

    def test_if_private_field_in_domain__raise_error(self):
        fields = [{'name': 'name'}]
        domain = [('sinid', '>', '123')]
        with pytest.raises(AccessError):
            self._export(ids=None, domain=domain, fields=fields)

    @data(
        'employee_ids/sinid',
        'employee_ids/address_home_id',
        'employee_ids/address_home_id/street',
    )
    def test_if_private_field_in_related_model_fields__raise_error(self, field):
        fields = [{'name': field}]
        with pytest.raises(AccessError):
            self._export(ids=None, domain=[], fields=fields, model='res.users')
