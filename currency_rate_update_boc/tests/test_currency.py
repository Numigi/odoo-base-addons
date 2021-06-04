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


@ddt
class TestBocRateProvider(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.cad = cls.env.ref("base.CAD")
        cls.cad.active = True

        cls.date = date(2021, 5, 3)
        cls.date_string = cls.date.strftime("%Y-%m-%d")

        cls.provider = cls.env["res.currency.rate.provider"].create(
            {"service": "bank_of_canada", "currency_ids": [(4, cls.cad.id)]}
        )

        cls.test_boc_url = "https://www.bankofcanada.ca/valet/observations/FXUSDCAD,FXEURCAD?start_date=2021-05-03&end_date=2021-05-03"

    @data("CAD", "USD", "EUR")
    def test_supported_currencies(self, currency_code):
        supported_currencies = self.provider.available_currency_ids.mapped("name")
        assert currency_code in supported_currencies

    def test_boc_response(self):
        json_data = self._get_rates_json()
        with requests_mock.Mocker() as m:
            m.get(self.test_boc_url, json=json_data)
            rates = self.provider._get_boc_response(self.test_boc_url).json()
            assert rates == json_data

    @data(401, 404, 410, 500, 502)
    def test_boc_response_exceptions(self, error_code):
        with requests_mock.Mocker() as m:
            m.get(self.test_boc_url, status_code=error_code)
            with pytest.raises(ValidationError):
                self.provider._get_boc_response(self.test_boc_url)

    def test_rates_cad2x(self):
        rates = self.provider._obtain_rates("CAD", ["USD", "EUR"], self.date, self.date)
        assert rates[self.date_string]["USD"] == round(1 / 1.2279, 4)
        assert rates[self.date_string]["EUR"] == round(1 / 1.4808, 4)

    def test_rates_x2cad(self):
        rates = self.provider._obtain_rates("USD", ["CAD"], self.date, self.date)
        assert rates[self.date_string]["CAD"] == 1.2279

    def test_rates_x2x(self):
        rates = self.provider._obtain_rates("USD", ["EUR"], self.date, self.date)
        assert rates[self.date_string]["EUR"] == round(1.2279 * 1 / 1.4808, 4)

    def test_invalid_currency(self):
        with pytest.raises(ValidationError):
            rates = self.provider._obtain_rates("USD", ["ZZZZ"], self.date, self.date)

    def test_invalid_date(self):
        with pytest.raises(ValidationError):
            rates = self.provider._obtain_rates("USD", ["ZZZZ"], self.date, self.date - timedelta(5))

    def _get_rates_json(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{dir_path}/FX_RATES.json") as f:
            data = json.load(f)
            return data
