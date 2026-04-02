# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.web.controllers.dataset import DataSet
from odoo.http import request
from odoo.osv.expression import AND

SEARCH_METHODS = [
    "name_search",
    "search",
    "search_count",
    "search_read",
    "read_group",
    "web_search_read",
]

DOMAIN_ARGUMENT_NAMES = {
    "name_search": "args",
    "search": "domain",
    "search_count": "domain",
    "search_read": "domain",
    "web_search_read": "domain",
    "read_group": "domain",
}

DOMAIN_ARGUMENT_INDEXES = {
    "name_search": 1,
    "search": 0,
    "search_count": 0,
    "search_read": 0,
    "web_search_read": 0,
    "read_group": 0,
}


class DataSetWithExtendedSearchSecurity(DataSet):
    """ Add extra security domains to search operations intercepting RPC calls. """

    def call_kw(self, model, method, args, kwargs):
        """ Override standard call_kw to inject security domains on search methods. """
        if method in SEARCH_METHODS:
            security_domain = _get_extended_security_domain(model)
            search_domain = get_domain_from_args_and_kwargs(method, args, kwargs)
            complete_domain = AND((search_domain, security_domain))
            args, kwargs = _get_args_and_kwargs_with_new_domain(
                method, args, kwargs, complete_domain
            )
        return super().call_kw(model, method, args, kwargs)


def _get_extended_security_domain(model):
    """ Get the security domain generated for the current model and user. """
    return request.env[model].get_extended_security_domain()


def get_domain_from_args_and_kwargs(method, args, kwargs):
    """
    Get the domain from the given args and kwargs.
    If neither the args or kwargs contain the domain, an empty domain is returned.
    """
    argument_name = DOMAIN_ARGUMENT_NAMES.get(method)
    argument_index = DOMAIN_ARGUMENT_INDEXES.get(method)

    args = args or []
    kwargs = kwargs or {}

    if argument_index is not None and len(args) > argument_index:
        return args[argument_index]

    if argument_name:
        return kwargs.get(argument_name) or []

    return []


def _get_args_and_kwargs_with_new_domain(method, args, kwargs, domain):
    """
    Get the args and kwargs updated with the new security domain.
    """
    argument_name = DOMAIN_ARGUMENT_NAMES.get(method)
    argument_index = DOMAIN_ARGUMENT_INDEXES.get(method)

    args = args or []
    kwargs = kwargs or {}

    if argument_index is not None and len(args) > argument_index:
        args = list(args)
        args[argument_index] = domain
    elif argument_name:
        kwargs = dict(kwargs)
        kwargs[argument_name] = domain

    return args, kwargs