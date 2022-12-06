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


DOMAIN_ARGUMENT_NAMES = {
    'name_search': 'args',
    'search': 'args',
    'search_count': 'args',
    'search_read': 'domain',
    'read_group': 'domain',
}


DOMAIN_ARGUMENT_INDEXES = {
    'name_search': 1,
    'search': 0,
    'search_count': 0,
    'search_read': 0,
    'read_group': 0,
}


class DataSetWithExtendedSearchSecurity(DataSet):
    """Add extra security domains to search operations."""

    def do_search_read(
        self, model, fields=False, offset=0, limit=False, domain=None, sort=None
    ):
        search_domain = domain or []
        security_domain = _get_extended_security_domain(model)
        complete_domain = AND([search_domain, security_domain])
        return super().do_search_read(
            model, fields=fields, offset=offset, limit=limit, domain=complete_domain, sort=sort
        )

    def _call_kw(self, model, method, args, kwargs):
        if method in SEARCH_METHODS:
            security_domain = _get_extended_security_domain(model)
            search_domain = get_domain_from_args_and_kwargs(method, args, kwargs)
            complete_domain = AND((search_domain, security_domain))
            args, kwargs = _get_args_and_kwargs_with_new_domain(
                method, args, kwargs, complete_domain)

        return super()._call_kw(model, method, args, kwargs)


def _get_extended_security_domain(model):
    return request.env[model].get_extended_security_domain()


def get_domain_from_args_and_kwargs(method, args, kwargs):
    """Get the domain from the given args and kwargs.

    If neither the args or kwargs contain the domain (which is a valid case),
    an empty domain is returned.

    :param method: the method called.
    :param args: the arguments passed through rpc.
    :param kargs: the keyword arguments passed through rpc.
    :return: the given domain.
    """
    argument_name = DOMAIN_ARGUMENT_NAMES[method]
    argument_index = DOMAIN_ARGUMENT_INDEXES[method]

    args = args or []
    kwargs = kwargs or {}

    if len(args) > argument_index:
        return args[argument_index]

    return kwargs.get(argument_name) or []


def _get_args_and_kwargs_with_new_domain(method, args, kwargs, domain):
    """Get the args and kwargs with a new domain.

    This function returns args and kwargs with the smallest changes possible.

    If the domain was previously contained in args, then a new args list
    is generated with the new domain.

    If the domain was previously contained in kwargs, then a new kwargs dict
    is generated with the new domain.

    If neither the args or kwargs contain a domain, it is set in kwargs.

    :param method: the method called.
    :param args: the arguments passed through rpc.
    :param kargs: the keyword arguments passed through rpc.
    :param domain: the new domain.
    :return: the args and kwargs containing the new domain.
    """
    argument_name = DOMAIN_ARGUMENT_NAMES[method]
    argument_index = DOMAIN_ARGUMENT_INDEXES[method]

    args = args or []
    kwargs = kwargs or {}

    if len(args) > argument_index:
        args = (
            args[:argument_index] + [domain] +
            args[argument_index + 1:]
        )

    else:
        kwargs = dict(kwargs)
        kwargs[argument_name] = domain

    return args, kwargs
