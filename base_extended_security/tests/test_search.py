# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt
from odoo.tests.common import TransactionCase
from odoo.addons.test_http_request.common import mock_odoo_request
from ..controllers.search import DataSetWithExtendedSearchSecurity


@ddt
class TestControllers(TransactionCase):
    def setUp(self):
        super().setUp()
        self.controller = DataSetWithExtendedSearchSecurity()

    def _read_group(self, domain, fields, groupby, domain_kwarg):
        with mock_odoo_request(self.env):
            if domain_kwarg:
                args = []
                kwargs = {
                    "domain": domain,
                    "fields": fields,
                    "groupby": groupby,
                    "orderby": groupby,
                }
            else:
                args = [domain, [], fields, groupby]
                kwargs = {"orderby": groupby}

            return self.controller.call_kw("res.partner", "read_group", args, kwargs)

    def _search(self, domain, domain_kwarg):
        with mock_odoo_request(self.env):
            args = [] if domain_kwarg else [domain]
            kwargs = {"domain": domain} if domain_kwarg else {}
            return self.controller.call_kw("res.partner", "search", args, kwargs)

    def _name_search(self, name, domain, name_kwarg, domain_kwarg):
        with mock_odoo_request(self.env):
            args = []
            kwargs = {}

            if name_kwarg:
                kwargs["name"] = name
            else:
                args.append(name)

            if domain_kwarg:
                kwargs["args"] = domain
            else:
                args.append(domain)

            name_get = self.controller.call_kw(
                "res.partner", "name_search", args, kwargs
            )
            return [r[0] for r in name_get]

    def _search_count(self, domain, domain_kwarg):
        with mock_odoo_request(self.env):
            args = [] if domain_kwarg else [domain]
            kwargs = {"domain": domain} if domain_kwarg else {}
            return self.controller.call_kw("res.partner", "search_count", args, kwargs)

    def _search_read(self, domain, use_search_read_route, domain_kwarg):
        with mock_odoo_request(self.env):
            if use_search_read_route:
                result = self.controller.search_read(
                    "res.partner", fields=[], domain=domain
                )
                records = result["records"]
            elif domain_kwarg:
                records = self.controller.call_kw(
                    "res.partner", "search_read", [domain, []], {}
                )
            else:
                records = self.controller.call_kw(
                    "res.partner", "search_read", [], {"domain": domain}
                )

            return [r["id"] for r in records]
