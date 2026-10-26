# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
import os
from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import requests
from ddt import data, ddt

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


@ddt
class TestBocRateProvider(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Activate required currencies for the tests
        cls.cad = cls.env.ref("base.CAD")
        cls.cad.active = True
        cls.usd = cls.env.ref("base.USD")
        cls.usd.active = True
        cls.eur = cls.env.ref("base.EUR")
        cls.eur.active = True

        cls.company = cls.env["res.company"].create({"name": "Test Company BOC"})
        cls.company.currency_id = cls.usd

        # Initialize the provider and link the currencies
        cls.provider = cls.env["res.currency.rate.provider"].create(
            {
                "service": "bank_of_canada",
                "currency_ids": [(4, cls.cad.id), (4, cls.usd.id), (4, cls.eur.id)],
                "company_id": cls.company.id,
            }
        )

        cls.date = date(2021, 5, 3)
        cls.date_string = cls.date.strftime("%Y-%m-%d")

        cls.test_boc_url = (
                               "https://www.bankofcanada.ca/valet/observations/"
                               "FXUSDCAD,FXEURCAD?start_date=%s&end_date=%s"
                           ) % (cls.date_string, cls.date_string)

        cls.dumb_test_boc_url = "https://www.bankofcanada.ca/valet/observations/"

    def _get_rates_json(self):
        """Helper to load the mock JSON response from the test directory."""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, "FX_RATES.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @data("CAD", "USD", "EUR")
    def test_supported_currencies(self, currency_code):
        """Ensure specific currencies are available in the provider's selection."""
        supported_currencies = self.provider.available_currency_ids.mapped("name")
        self.assertIn(currency_code, supported_currencies)

    @patch("odoo.addons.currency_rate_update_boc.models.res_currency_rate_provider.requests.get")
    def test_boc_response(self, mock_get):
        """Test proper JSON parsing of a successful API response."""
        json_data = self._get_rates_json()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = json_data
        mock_get.return_value = mock_response

        rates = self.provider._get_boc_response(self.test_boc_url).json()
        self.assertEqual(rates, json_data)

    @data(401, 404, 410, 500, 502)
    @patch("odoo.addons.currency_rate_update_boc.models.res_currency_rate_provider.requests.get")
    def test_boc_response_exceptions(self, error_code, mock_get):
        """Ensure HTTP errors are properly caught and raised as ValidationError."""
        mock_response = MagicMock()
        mock_response.status_code = error_code
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("API Error")
        mock_get.return_value = mock_response

        with self.assertRaises(ValidationError):
            self.provider._get_boc_response(self.dumb_test_boc_url)

    @patch("odoo.addons.currency_rate_update_boc.models.res_currency_rate_provider.requests.get")
    def test_rates_cad2x(self, mock_get):
        """Test exchange rate calculation when the base currency is CAD."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self._get_rates_json()
        mock_get.return_value = mock_response

        rates = self.provider._obtain_rates("CAD", ["USD", "EUR"], self.date, self.date)

        # 1 CAD = 1 / FXUSDCAD USD
        self.assertEqual(rates[self.date_string]["USD"], round(1 / 1.2279, 4))
        self.assertEqual(rates[self.date_string]["EUR"], round(1 / 1.4808, 4))

    @patch("odoo.addons.currency_rate_update_boc.models.res_currency_rate_provider.requests.get")
    def test_rates_x2cad(self, mock_get):
        """Test exchange rate calculation when the target currency is CAD."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self._get_rates_json()
        mock_get.return_value = mock_response

        rates = self.provider._obtain_rates("USD", ["CAD"], self.date, self.date)

        # 1 USD = FXUSDCAD CAD
        self.assertEqual(rates[self.date_string]["CAD"], 1.2279)

    @patch("odoo.addons.currency_rate_update_boc.models.res_currency_rate_provider.requests.get")
    def test_rates_x2x(self, mock_get):
        """Test exchange rate calculation crossing two non-CAD currencies."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self._get_rates_json()
        mock_get.return_value = mock_response

        rates = self.provider._obtain_rates("USD", ["EUR"], self.date, self.date)

        # 1 USD = FXUSDCAD CAD. 1 EUR = FXEURCAD CAD.
        # So 1 USD = (FXUSDCAD / FXEURCAD) EUR
        self.assertEqual(rates[self.date_string]["EUR"], round(1.2279 / 1.4808, 4))

    @patch("odoo.addons.currency_rate_update_boc.models.res_currency_rate_provider.requests.get")
    def test_invalid_currency(self, mock_get):
        """Verify the module blocks unknown or invalid currency formats."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")
        mock_get.return_value = mock_response

        with self.assertRaises(ValidationError):
            self.provider._obtain_rates("USD", ["ZZZZ"], self.date, self.date)

    @patch("odoo.addons.currency_rate_update_boc.models.res_currency_rate_provider.requests.get")
    def test_invalid_date(self, mock_get):
        """Verify the module blocks inverted or invalid date ranges."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Bad Request")
        mock_get.return_value = mock_response

        with self.assertRaises(ValidationError):
            self.provider._obtain_rates(
                "USD", ["ZZZZ"], self.date, self.date - timedelta(days=5)
            )

    @patch("odoo.addons.currency_rate_update_boc.models.res_currency_rate_provider.requests.get")
    def test_cron_loads_rates_one_day_prior(self, mock_get):
        """Ensure the scheduled job successfully applies rates covering the correct date."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self._get_rates_json()
        mock_get.return_value = mock_response

        self.provider.last_successful_run = self.date
        self.provider.next_run = self.date + timedelta(days=1)

        # Using OCA's standard _scheduled_update trigger
        self.env["res.currency.rate.provider"]._scheduled_update()

        rate = self.cad._get_rates(self.company, self.date)[self.cad.id]
        self.assertEqual(round(rate, 4), 1.2279)
