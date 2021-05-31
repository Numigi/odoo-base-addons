# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import requests
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from collections import defaultdict
from .currency import SUPPORTED_CURRENCIES_BOC, API_ADDRESS


class ResCurrencyRateProvider(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(selection_add=[("bank_of_canada", "Bank of canada")])

    @api.multi
    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != "bank_of_canada":
            return super()._get_supported_currencies()
        return SUPPORTED_CURRENCIES_BOC

    @api.multi
    def _obtain_rates(self, base_currency, currencies, date_from, date_to):
        self.ensure_one()
        if self.service != "bank_of_canada":
            return super()._obtain_rates(base_currency, currencies, date_from, date_to)

        observations = self._get_rates_from_boc(date_from, date_to)
        result = defaultdict(dict)

        for currency in currencies:
            for date, rate in self._iter_rate_from_boc_observations(
                observations, base_currency, currency
            ):
                result[date][currency] = rate

        return result

    def _get_rates_from_boc(self, date_from, date_to):
        response = requests.request("GET", API_ADDRESS)
        if response.status_code >= 400:
            raise ValidationError(
                _(
                    "The request to the Valet api of the Bank of Canada terminated with an error.\n\n{}".format(
                        response.text
                    )
                )
            )

        observations = response.json()["observations"]
        date_from = date_from.strftime("%Y-%m-%d")
        date_to = date_to.strftime("%Y-%m-%d")

        return [o for o in observations if date_from <= o["d"] <= date_to]

    def _iter_rate_from_boc_observations(self, observations, base_currency, currency):
        if base_currency == "CAD":
            yield from self._iter_cad2x(observations, currency)
        elif currency == "CAD":
            yield from self._iter_x2cad(observations, base_currency)
        else:
            yield from self._iter_x2x(observations, base_currency, currency)

    def _iter_cad2x(self, observations, currency):
        exchange = f"FX{currency}CAD"
        for observation in observations:
            if exchange in observation:
                rate = float(observation[exchange]["v"])
                yield observation["d"], round(rate, 4)

    def _iter_x2cad(self, observations, currency):
        exchange = f"FX{currency}CAD"
        for observation in observations:
            if exchange in observation:
                rate = 1 / float(observation[exchange]["v"])
                yield observation["d"], round(rate, 4)

    def _iter_x2x(self, observations, base_currency, currency):
        first_exchange = f"FX{base_currency}CAD"
        second_exchange = f"FX{currency}CAD"
        for observation in observations:
            if first_exchange in observation and second_exchange in observation:
                rate = (
                    1
                    / float(observation[first_exchange]["v"])
                    * float(observation[second_exchange]["v"])
                )
                yield observation["d"], round(rate, 4)
