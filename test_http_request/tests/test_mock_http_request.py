# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from collections import OrderedDict
from ddt import data, ddt, unpack
from odoo.http import request
from odoo.tests import common
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.urls import url_encode
from ..common import mock_odoo_request


@ddt
class TestMockHttpRequest(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.data = OrderedDict([
            ('firstname', 'John'),
            ('lastname', 'Doe'),
        ])

    def test_env_propagated_to_request(self):
        with mock_odoo_request(self.env, data=self.data):
            assert request.env == self.env

    def test_method_propagated_to_request(self):
        method = 'PATCH'
        with mock_odoo_request(self.env, data=self.data, method=method):
            assert request.request.method == method

    def test_headers_propagated_to_request(self):
        header_key = 'Some-Header'
        header_value = 'some value'
        headers = {
            header_key: header_value,
        }
        with mock_odoo_request(self.env, data=self.data, headers=headers):
            assert request.request.headers[header_key] == header_value

    @data(
        ('http', 'application/x-www-form-urlencoded'),
        ('json', 'application/json'),
    )
    @unpack
    def test_content_type(self, routing_type, content_type):
        with mock_odoo_request(self.env, data=self.data, routing_type=routing_type):
            assert request.request.content_type == content_type

    def test_if_http_routing__data_contained_in_request_form(self):
        with mock_odoo_request(self.env, data=self.data):
            assert request.request.form == ImmutableMultiDict(self.data)
            assert not request.request.data

    def test_if_json_routing__data_contained_in_request_data(self):
        json_data = json.dumps(self.data).encode()
        with mock_odoo_request(self.env, data=self.data, routing_type='json'):
            assert not request.request.form
            assert request.request.data == json_data

    def test_form_data_propagated_with_correct_key_order(self):
        data = OrderedDict([(str(i), str(i)) for i in range(10)])
        with mock_odoo_request(self.env, data=data):
            assert url_encode(request.request.form) == url_encode(data)
