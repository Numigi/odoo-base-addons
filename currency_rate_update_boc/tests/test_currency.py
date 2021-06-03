# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import requests_mock
import json
import os
import pytest
from datetime import date, timedelta
from odoo.tests.common import SavepointCase
from ddt import ddt, data
from odoo.exceptions import ValidationError
from ..models.currency import BASE_API_ADDRESS


@ddt
class TestBocRateProvider(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.cad = cls.env.ref("base.CAD")
        cls.cad.active = True

        cls.date = date(2021, 5, 28)
        cls.date_string = cls.date.strftime("%Y-%m-%d")

        cls.provider = cls.env["res.currency.rate.provider"].create(
            {"service": "bank_of_canada", "currency_ids": [(4, cls.cad.id)]}
        )

    @data("CAD", "USD", "EUR")
    def test_supported_currencies(self, currency_code):
        supported_currencies = self.provider.available_currency_ids.mapped("name")
        assert currency_code in supported_currencies

    def test_get_rates(self):
        json_data = self._get_rates_json()
        with requests_mock.Mocker() as m:
            m.get(BASE_API_ADDRESS, json=json_data)
            rates = self.provider._get_rates_from_boc(self.date, self.date)
            assert rates == json_data["observations"]

    @data(401, 404, 410, 500, 502)
    def test_get_rates_exceptions(self, error_code):
        with requests_mock.Mocker() as m:
            m.get(BASE_API_ADDRESS, status_code=error_code)
            with pytest.raises(ValidationError):
                self.provider._get_rates_from_boc(self.date, self.date)

    def test_rates_filtered_cad2x(self):
        json_data = self._get_rates_json()
        with requests_mock.Mocker() as m:
            m.get(BASE_API_ADDRESS, status_code=200, json=json_data)
            filtered_rates = self.provider._obtain_rates(
                "CAD", ["USD", "EUR"], self.date, self.date
            )
            assert filtered_rates[self.date_string]["USD"] == 1.2086
            assert filtered_rates[self.date_string]["EUR"] == 1.4723

    def test_rates_filtered_x2cad(self):
        json_data = self._get_rates_json()
        with requests_mock.Mocker() as m:
            m.get(BASE_API_ADDRESS, status_code=200, json=json_data)
            filtered_rates = self.provider._obtain_rates(
                "USD", ["CAD"], self.date, self.date
            )
            assert filtered_rates[self.date_string]["CAD"] == round(1 / 1.2086, 4)

    def test_rates_filtered_x2x(self):
        json_data = self._get_rates_json()
        with requests_mock.Mocker() as m:
            m.get(BASE_API_ADDRESS, status_code=200, json=json_data)
            filtered_rates = self.provider._obtain_rates(
                "USD", ["EUR"], self.date, self.date
            )
            assert filtered_rates[self.date_string]["EUR"] == round(
                1 / 1.2086 * 1.4723, 4
            )

    def test_invalid_currency(self):
        json_data = self._get_rates_json()
        with requests_mock.Mocker() as m:
            m.get(BASE_API_ADDRESS, status_code=200, json=json_data)
            filtered_rates = self.provider._obtain_rates(
                "CAD", ["ZZZZ"], self.date, self.date
            )
            assert not filtered_rates

    def test_invalid_date(self):
        json_data = self._get_rates_json()
        with requests_mock.Mocker() as m:
            m.get(BASE_API_ADDRESS, status_code=200, json=json_data)
            filtered_rates = self.provider._obtain_rates(
                "CAD", ["USD", "EUR"], self.date, self.date - timedelta(5)
            )
            assert not filtered_rates

    def _get_rates_json(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{dir_path}/FX_RATES_DAILY.json") as f:
            data = json.load(f)
            return data
