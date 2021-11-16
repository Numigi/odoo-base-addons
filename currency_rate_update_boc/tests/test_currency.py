# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import requests_mock
import json
import os
import pytest
from contextlib import contextmanager
from datetime import date, timedelta
from odoo.tests.common import SavepointCase
from ddt import ddt, data
from odoo.exceptions import ValidationError


@ddt
class TestBocRateProvider(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.company = cls.env.user.company_id

        cls.cad = cls.env.ref("base.CAD")
        cls.cad.active = True

        cls.date = date(2021, 5, 3)
        cls.date_string = cls.date.strftime("%Y-%m-%d")

        cls.provider = cls.env["res.currency.rate.provider"].create(
            {"service": "bank_of_canada", "currency_ids": [(4, cls.cad.id)]}
        )

        cls.test_boc_url = "https://www.bankofcanada.ca/valet/observations/"

    @data("CAD", "USD", "EUR")
    def test_supported_currencies(self, currency_code):
        supported_currencies = self.provider.available_currency_ids.mapped("name")
        assert currency_code in supported_currencies

    def test_boc_response(self):
        with self._mock_boc_response(["FXUSDCAD"]):
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

    def test_cron__loads_rates_one_day_prior(self):
        """Test that the rates of yesterday are loaded by the cron.

        With the Bank of Canada, the daily rates are only available the day after.
        When the cron is executed the rates of the current date are not available.

        The rates of the current date are loaded the following day.
        Otherwise, the cron ends up loading no rate at all.
        """
        self.provider.last_successful_run = self.date
        self.provider.next_run = self.date + timedelta(1)
        with self._mock_boc_response(["FXUSDCAD"]):
            self.env["res.currency.rate.provider"]._scheduled_update()
        rate = self.cad._get_rates(self.company, self.date)[self.cad.id]
        assert round(rate, 4) == 1.2279

    @contextmanager
    def _mock_boc_response(self, series):
        json_data = self._get_rates_json()
        with requests_mock.Mocker() as m:
            url = self.test_boc_url + ",".join(series)
            m.get(url, json=json_data)
            yield

    def _get_rates_json(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{dir_path}/FX_RATES.json") as f:
            data = json.load(f)
            return data
