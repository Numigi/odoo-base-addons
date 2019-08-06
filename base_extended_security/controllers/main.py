# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.web.controllers.main import DataSet
from odoo.http import request
from odoo.osv.expression import AND

SEARCH_METHODS = [
    'name_search',
    'search',
    'search_count',
    'search_read',
    'read_group',
]


class DataSetWithExtendedSearchSecurity(DataSet):
    """Add extra security domains to search operations."""

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
            domain_index = 1 if method == 'name_search' else 0
            search_domain = args[domain_index]
            complete_domain = AND((search_domain, security_domain))
            args = args[:domain_index] + [complete_domain] + args[domain_index + 1:]

        return super()._call_kw(model, method, args, kwargs)


READ_WRITE_UNLINK_METHODS = [
    'read',
    'name_get',
    'write',
    'unlink',
]


CREATE_METHODS = [
    'create',
    'name_create',
]


class DataSetWithExtendedSecurity(DataSetWithExtendedSearchSecurity):
    """Add extra security rules for read/write/create/unlink operations."""

    def _check_extended_security_rules(self, model, method, record_ids):
        records = request.env[model].browse(record_ids)
        records.check_extended_security_all()
        getattr(records, 'check_extended_security_{}'.format(method))()

    def _call_kw(self, model, method, args, kwargs):
        if method in READ_WRITE_UNLINK_METHODS:
            record_ids = args[0]
            method_to_check = 'read' if method == 'name_get' else method
            self._check_extended_security_rules(model, method_to_check, record_ids)

        result = super()._call_kw(model, method, args, kwargs)

        if method in CREATE_METHODS:
            record_ids = [result[0]] if method == 'name_create' else result
            self._check_extended_security_rules(model, 'create', record_ids)

        return result
