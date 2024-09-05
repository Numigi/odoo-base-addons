# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data, unpack
from odoo.addons.test_http_request.common import mock_odoo_request
from .common import ControllerCase
from ..controllers.search import DataSetWithExtendedSearchSecurity


@ddt
class TestControllers(ControllerCase):

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

    @data(True, False)
    def test_read_group_with_empty_domain(self, domain_kwarg):
        groups = self._read_group(
            [],
            fields=["customer_rank"],
            groupby="customer_rank",
            domain_kwarg=domain_kwarg,
        )
        assert len(groups) == 1
        assert groups[0]["customer_rank_count"] == self.customer_count

    @data(True, False)
    def test_read_group_with_supplier_domain(self, domain_kwarg):
        domain = [("supplier_rank", ">", 0)]
        groups = self._read_group(
            domain,
            fields=["customer_rank"],
            groupby="customer_rank",
            domain_kwarg=domain_kwarg,
        )
        assert len(groups) == 1
        assert groups[0]["customer_rank_count"] == self.supplier_customer_count

    def _search(self, domain, domain_kwarg):
        with mock_odoo_request(self.env):
            args = [] if domain_kwarg else [domain]
            kwargs = {"domain": domain} if domain_kwarg else {}
            return self.controller.call_kw("res.partner", "search", args, kwargs)

    @data(True, False)
    def test_search_with_empty_domain(self, domain_kwarg):
        ids = self._search([], domain_kwarg)
        assert self.customer.id in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    @data(True, False)
    def test_search_with_supplier_domain(self, domain_kwarg):
        ids = self._search([("supplier_rank", ">", 0)], domain_kwarg)
        assert self.customer.id not in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

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

    @data(
        (True, True),
        (False, False),
        (False, True),
    )
    @unpack
    def _test_name_search_with_empty_domain(self, name_kwarg, domain_kwarg):
        ids = self._name_search("My Partner", [], name_kwarg, domain_kwarg)
        assert self.customer.id in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    @data(
        (True, True),
        (False, False),
        (False, True),
    )
    @unpack
    def test_name_search_with_supplier_domain(self, name_kwarg, domain_kwarg):
        ids = self._name_search(
            "My Partner", [("supplier_rank", ">", 0)], name_kwarg, domain_kwarg
        )
        assert self.customer.id not in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    def _search_count(self, domain, domain_kwarg):
        with mock_odoo_request(self.env):
            args = [] if domain_kwarg else [domain]
            kwargs = {"domain": domain} if domain_kwarg else {}
            return self.controller.call_kw("res.partner", "search_count", args, kwargs)

    @data(True, False)
    def test_search_count_with_empty_domain(self, domain_kwarg):
        count = self._search_count([], domain_kwarg)
        assert count == self.customer_count

    @data(True, False)
    def test_search_count_with_supplier_domain(self, domain_kwarg):
        count = self._search_count([("supplier_rank", ">", 0)], domain_kwarg)
        assert count == self.supplier_customer_count

    def _search_read(self, domain, use_search_read_route, domain_kwarg):
        with mock_odoo_request(self.env):
            if use_search_read_route:
                result = self.controller.search_read(
                    "res.partner", fields=[], domain=domain
                )
                records = result["records"]
                print("if ",domain)
            elif domain_kwarg:
                records = self.controller.call_kw(
                    "res.partner", "search_read", [domain, []],{}
                )
                print("eif ", domain)
            else:
                records = self.controller.call_kw(
                    "res.partner", "search_read", [], {"domain": domain}
                )
                print("else ", domain)

            return [r["id"] for r in records]

    @data(
        (True, False),
        (False, False),
        (False, True),
    )
    @unpack
    def test_search_read_with_empty_domain(self, use_search_read_route, domain_kwarg):
        ids = self._search_read([], use_search_read_route, domain_kwarg)
        print("ids",ids)
        assert self.customer.id in ids
        assert self.supplier.id not in ids
        assert self.supplier_customer.id in ids

    # @data(
    #     (True, False),
    #     (False, False),
    #     (False, True),
    # )
    # @unpack
    # def test_search_read_with_supplier_domain(
    #     self, use_search_read_route, domain_kwarg
    # ):
    #     ids = self._search_read(
    #         [("supplier_rank", ">", 0)], use_search_read_route, domain_kwarg
    #     )
    #     assert self.customer.id not in ids
    #     assert self.supplier.id not in ids
    #     assert self.supplier_customer.id in ids
