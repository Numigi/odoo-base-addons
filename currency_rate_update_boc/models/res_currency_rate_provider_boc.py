# -*- coding: utf-8 -*-
# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import requests
from odoo import api, fields, models
from collections import defaultdict


class ResCurrencyRateProviderBOC(models.Model):
    _inherit = 'res.currency.rate.provider'

    service = fields.Selection(
        selection_add=[('BOC', 'Bank of canada')]
    )

    @api.multi
    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != 'BOC':
            return super()._get_supported_currencies()  # pragma: no cover

        CurrencyObj = self.env['res.currency']

        currency_name = [
            currency.name for currency in CurrencyObj.search([])
        ]
        return currency_name

    @api.multi
    def _obtain_rates(self, base_currency, currency_names, date_from, date_to):
        """
	        This method is used to update currencies exchange rate
	        by using Bank Of Canada.
        """
        self.ensure_one()
        if self.service != 'BOC':
            return super()._obtain_rates(
                base_currency,
                currency_names,
                date_from,
                date_to
            )  # pragma: no cover

        bankofcanada_url = "http://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json"
        try:
            response = requests.request('GET', bankofcanada_url)
        except:
            return False

        data = response.json()
        content = defaultdict(dict)
        date_from_formated = date_from.strftime("%Y-%m-%d")
        date_to_formated = date_to.strftime("%Y-%m-%d")

        # To filtered currencies by observations
        currency_bankofcanada_names = []
        for currency_name in currency_names:
            currency_bankofcanada_names.append('FX%sCAD' % currency_name)

        #  recent[_interval] cannot be used at the same time as the start_date and end_date parameters. 
        # 'observations' key contains rates observations by date

        observations = [obs for obs in data['observations'] if date_to_formated >= obs['d'] >= date_from_formated]

        for obs in observations:
            ObsFiltered = {k: v for k, v in obs.items() if k in currency_bankofcanada_names + ['d']}
            for key, value in ObsFiltered.items():
                if 'd' in key:
                    date = value
                    continue

                for currency_name in currency_names:
                    if key == ('FX{}CAD'.format(currency_name)):
                        content[date][currency_name] = str(1.0 / float(value['v']))
        return content
