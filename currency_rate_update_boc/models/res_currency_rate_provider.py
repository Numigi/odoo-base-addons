# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict
from datetime import timedelta
import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from .currency import BASE_API_ADDRESS, SUPPORTED_CURRENCIES_BOC


class ResCurrencyRateProvider(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(
        selection_add=[("bank_of_canada", "Bank of Canada")],
        ondelete={"bank_of_canada": "set default"},
    )

    def _get_supported_currencies(self):
        """Override to return supported currencies specifically for BoC."""
        self.ensure_one()
        if self.service != "bank_of_canada":
            return super()._get_supported_currencies()
        return SUPPORTED_CURRENCIES_BOC

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        """Fetch rates from the Bank of Canada API for the requested period."""
        self.ensure_one()
        if self.service != "bank_of_canada":
            return super()._obtain_rates(base_currency, currencies, date_from, date_to)

        # BoC provides rates at the end of the day, querying requires going back one day
        target_date_from = date_from - timedelta(days=1)
        observations = self._get_rates_from_boc(
            base_currency, currencies, target_date_from, date_to
        ).get("observations", [])

        return self._process_observations(observations, base_currency, currencies)

    def _get_rates_from_boc(self, base_currency, currencies, date_from, date_to):
        """Build the URL and fetch the JSON response from BoC."""
        url = self._get_boc_url(base_currency, currencies, date_from, date_to)
        response = self._get_boc_response(url)
        return response.json()

    def _get_boc_url(self, base_currency, currencies, date_from, date_to):
        """Construct the specific endpoint URL for the required currencies and date range."""
        str_date_from = date_from.strftime("%Y-%m-%d")
        str_date_to = date_to.strftime("%Y-%m-%d")

        exchanges = {
            series for series in self._iter_boc_series(base_currency, currencies)
        }
        date_filter = f"start_date={str_date_from}&end_date={str_date_to}"
        return f"{BASE_API_ADDRESS}{','.join(exchanges)}?{date_filter}"

    def _iter_boc_series(self, base_currency, currencies):
        """
        Generate the series names. BoC always provides rates relative to CAD.
        Format is always FX{CURRENCY}CAD.
        """
        if base_currency != "CAD":
            yield f"FX{base_currency}CAD"

        for currency in set(currencies):
            if currency != "CAD":
                yield f"FX{currency}CAD"

    def _get_boc_response(self, url):
        """Execute the HTTP GET request and validate the status."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise ValidationError(
                _(
                    "The request to the Valet API of the Bank of Canada failed.\n\n"
                    "Error Details: %(error)s\nURL: %(url)s",
                    error=str(error),
                    url=url,
                )
            )
        return response

    def _process_observations(self, observations, base_currency, currencies):
        """Parse the JSON observations and format them for Odoo's currency update engine."""
        result = defaultdict(dict)
        for observation in observations:
            obs_date = observation.get("d")
            if not obs_date:
                continue

            for currency in currencies:
                rate = self._get_rate_from_boc_observation(
                    observation, base_currency, currency
                )
                if rate:
                    result[obs_date][currency] = round(rate, 4)
        return result

    def _get_rate_from_boc_observation(self, observation, base_currency, currency):
        """Compute the exact rate for a specific currency pair using CAD as a pivot."""
        if base_currency == currency:
            return 1.0

        base_to_cad = 1.0
        if base_currency != "CAD":
            base_to_cad = self._get_rate_from_boc_series(observation, f"FX{base_currency}CAD")

        target_to_cad = 1.0
        if currency != "CAD":
            target_to_cad = self._get_rate_from_boc_series(observation, f"FX{currency}CAD")

        if base_to_cad and target_to_cad:
            # 1 BASE = base_to_cad CAD. 1 TARGET = target_to_cad CAD.
            # Therefore, 1 BASE = (base_to_cad / target_to_cad) TARGET
            return base_to_cad / target_to_cad

        return 0.0

    def _get_rate_from_boc_series(self, observation, series):
        """Safely retrieve and convert the rate value from the observation dictionary."""
        series_data = observation.get(series)
        if series_data and "v" in series_data:
            return float(series_data["v"])
        return 0.0
