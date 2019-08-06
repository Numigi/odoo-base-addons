# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.web.controllers.main import DataSet
from odoo.http import request
from odoo.osv.expression import AND

SEARCH_METHODS = {
    # Method Name: index of domain in args
    'name_search': 1,
    'search': 0,
    'search_count': 0,
    'search_read': 0,
    'read_group': 0,
}


class DataSetWithExtendedSecurity(DataSet):

    def _get_extended_security_domain(self, model):
        return request.env[model].get_extended_security_domain()

    def do_search_read(
        self, model, fields=False, offset=0, limit=False, domain=None, sort=None
    ):
        search_domain = domain or []
        security_domain = self._get_extended_security_domain(model)
        complete_domain = AND([search_domain, security_domain])
        return super().do_search_read(
            model, fields=fields, offset=offset, limit=limit, domain=complete_domain, sort=sort
        )

    def _call_kw(self, model, method, args, kwargs):
        if method in SEARCH_METHODS:
            security_domain = self._get_extended_security_domain(model)
            domain_index = SEARCH_METHODS[method]
            search_domain = args[domain_index]
            complete_domain = AND((search_domain, security_domain))
            args = (
                args[0:domain_index] + [complete_domain] + args[domain_index + 1:]
            )

        return super()._call_kw(model, method, args, kwargs)
