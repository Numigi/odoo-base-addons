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
            search_domain = get_domain_from_args_and_kwargs(method, args, kwargs)
            complete_domain = AND((search_domain, security_domain))
            args, kwargs = _get_args_and_kwargs_with_new_domain(
                method, args, kwargs, complete_domain)

        return super()._call_kw(model, method, args, kwargs)


class DataSetWithExtendedSecurity(DataSetWithExtendedSearchSecurity):
    """Add extra security rules for read/write/create/unlink operations."""

    def _call_kw(self, model, method, args, kwargs):
        if _is_read_request(method, args, kwargs):
            _check_read_rules(model, record_ids=args[0])

        elif _is_write_request(method):
            _check_write_rules(model, record_ids=args[0])

        elif _is_unlink_request(method):
            _check_unlink_rules(model, record_ids=args[0])

        result = super()._call_kw(model, method, args, kwargs)

        if _is_create_request(method):
            record_ids = [result[0]] if method == 'name_create' else result
            _check_create_rules(model, record_ids=record_ids)

        elif _is_write_request(method):
            _check_write_rules(model, record_ids=args[0])

        return result


def _check_read_rules(model, record_ids):
    records = _browse_records(model, record_ids)
    records.check_extended_security_read()
    records.check_extended_security_all()


def _check_write_rules(model, record_ids):
    records = _browse_records(model, record_ids)
    records.check_extended_security_write()
    records.check_extended_security_all()


def _check_create_rules(model, record_ids):
    records = _browse_records(model, record_ids)
    records.check_extended_security_create()
    records.check_extended_security_all()


def _check_unlink_rules(model, record_ids):
    records = _browse_records(model, record_ids)
    records.check_extended_security_unlink()
    records.check_extended_security_all()


def _is_unlink_request(method):
    return method == 'unlink'


def _is_create_request(method):
    return method in ('create', 'name_create')


def _is_write_request(method):
    return method == 'write'


def _is_read_request(method, args, kwargs):
    return method == 'read' and not _is_many2many_tag_read_request(method, args, kwargs)


def _is_many2many_tag_read_request(method, args, kwargs):
    if method != 'read':
        return False

    fields = set(_get_read_request_fields(args, kwargs))

    all_fields_requested = not fields
    if all_fields_requested:
        return False

    has_only_many2many_tag_fields = not fields.difference(('display_name', 'color'))
    return has_only_many2many_tag_fields


def _get_read_request_fields(args, kwargs):
    fields_args_index = 1
    return (
        args[fields_args_index]
        if len(args) > fields_args_index
        else kwargs.get('fields')
    )


def _browse_records(model, record_ids):
    return request.env[model].browse(record_ids)
