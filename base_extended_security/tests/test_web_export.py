# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import pytest
from unittest.mock import patch
from odoo.exceptions import AccessError
from .common import ControllerCase
from ..controllers.web_export import CSVControllerWithSecurity


class TestWebExport(ControllerCase):

    def setUp(self):
        super().setUp()
        self.controller = CSVControllerWithSecurity()

    def _export(self, ids, domain):
        params = {
            'model': 'res.partner',
            'ids': ids,
            'domain': domain,
            'import_compat': True,
            'fields': [{'name': 'name'}],
        }
        data_ = json.dumps(params)
        token = 'test1234'
        with patch(self.env):
            response = self.controller.base(data_, token)
            return response.data.decode('utf-8')

    def test_if_given_domain__domain_filter_applied_to_data(self):
        data_ = self._export(ids=[], domain=[])
        assert self.customer.name in data_
        assert self.supplier.name not in data_
        assert self.supplier_customer.name in data_

    def test_if_given_record_ids__and_not_access_all__raise_access_error(self):
        with pytest.raises(AccessError):
            self._export(ids=[self.employee.id], domain=[])

    def test_if_given_record_ids__and_not_access_read__raise_access_error(self):
        with pytest.raises(AccessError):
            self._export(ids=[self.supplier.id], domain=[])

    def test_if_given_record_ids__and_has_access_to_record__data_returned(self):
        ids = [self.customer.id, self.supplier_customer.id]
        data_ = self._export(ids=ids, domain=[])
        assert self.customer.name in data_
        assert self.supplier_customer.name in data_
