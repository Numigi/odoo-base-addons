# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import pytest
from odoo.exceptions import AccessError
from .common import ControllerCase, mock_request_env
from ..controllers.web_export import CSVControllerWithSecurity


class DummyResponse:
    """Faux objet de réponse pour capturer les données renvoyées par make_response"""

    def __init__(self, data):
        self.data = data


class TestWebExport(ControllerCase):
    def setUp(self):
        super().setUp()
        self.controller = CSVControllerWithSecurity()

    def _export(self, ids, domain):
        params = {
            "model": "res.partner",
            "ids": ids,
            "domain": domain,
            "import_compat": True,
            "fields": [{"name": "name"}],
        }
        data_ = json.dumps(params)

        with mock_request_env(self.env) as mock_req:
            # On configure le mock pour qu'il capture les données CSV générées
            mock_req.make_response.side_effect = (
                lambda data, *args, **kwargs: DummyResponse(data)
            )

            response = self.controller.base(data_)

            # Selon la version d'Odoo, le CSV peut être en bytes ou en string
            if isinstance(response.data, bytes):
                return response.data.decode("utf-8")
            return str(response.data)

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
