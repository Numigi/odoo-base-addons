# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import requests
from datetime import timedelta
from odoo import fields, models, _
from odoo.exceptions import ValidationError
from collections import defaultdict
from .currency import SUPPORTED_CURRENCIES_BOC, BASE_API_ADDRESS


class ResCurrencyRateProvider(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(
        selection_add=[("bank_of_canada", "Bank of canada")],
        ondelete={"bank_of_canada": 'set default'})

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != "bank_of_canada":
            return super()._get_supported_currencies()
        return SUPPORTED_CURRENCIES_BOC

    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service != "bank_of_canada":
            return super()._obtain_rates(base_currency, currencies, date_from, date_to)

        date_from = date_from - timedelta(1)
        observations = self._get_rates_from_boc(
            base_currency, currencies, date_from, date_to
        )["observations"]
        return self._process_observations(observations, base_currency, currencies)

    def _get_rates_from_boc(self, base_currency, currencies, date_from, date_to):
        url = self._get_boc_url(base_currency, currencies, date_from, date_to)
        response = self._get_boc_response(url)
        return response.json()

    def _get_boc_url(self, base_currency, currencies, date_from, date_to):
        date_from = date_from.strftime("%Y-%m-%d")
        date_to = date_to.strftime("%Y-%m-%d")
        exchanges = {s for s in self._iter_boc_series(
            base_currency, currencies)}
        date_filter = f"start_date={date_from}&end_date={date_to}"
        return f"{BASE_API_ADDRESS}{','.join(exchanges)}?{date_filter}"

    def _iter_boc_series(self, base_currency, currencies):
        for currency in sorted(currencies):
            if base_currency == "CAD" or currency == "CAD":
                yield f"FX{base_currency}{currency}"
            else:
                yield f"FX{base_currency}CAD"
                yield f"FXCAD{currency}"

    def _get_boc_response(self, url):
        response = requests.get(url)
        if response.status_code >= 400:
            raise ValidationError(
                _(
                    "The request to the Valet api of the Bank of Canada terminated with an error.\n\n{} : {}".format(
                        response.text, url
                    )
                )
            )

        return response

    def _process_observations(self, observations, base_currency, currencies):
        result = defaultdict(dict)
        for observation in observations:
            for currency in currencies:
                result[observation["d"]][currency] = round(
                    self._get_rate_from_boc_observation(
                        observation, base_currency, currency
                    ),
                    4,
                )

        return result

    def _get_rate_from_boc_observation(self, observation, base_currency, currency):
        if base_currency == "CAD" or currency == "CAD":
            series = f"FX{base_currency}{currency}"
            return self._get_rate_from_boc_series(observation, series)
        else:
            first_series = f"FX{base_currency}CAD"
            second_series = f"FXCAD{currency}"
            first_rate = self._get_rate_from_boc_series(
                observation, first_series)
            second_rate = self._get_rate_from_boc_series(
                observation, second_series)

            return first_rate * second_rate

    def _get_rate_from_boc_series(self, observation, series):
        return float(observation[series]["v"])
