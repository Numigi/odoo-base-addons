# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.web.controllers.main import DataSet
from odoo.addons.base_extended_security.controllers.search import (
    SEARCH_METHODS,
    get_domain_from_args_and_kwargs,
)
from odoo.http import request
from typing import Iterable
from .common import check_model_fields_access, extract_fields_from_domain


METHODS_WITH_ORDERBY = [
    'search',
    'search_read',
    'read_group',
]


ORDERBY_ARGUMENT_NAMES = {
    'search': 'order',
    'search_read': 'order',
    'read_group': 'orderby',
}


ORDERBY_ARGUMENT_INDEXES = {
    'search': 3,
    'search_read': 4,
    'read_group': 5,
}


def _get_orderby_from_args_and_kwargs(method: str, args: list, kwargs: dict):
    """Get the orderby from the given args and kwargs.

    If neither the args or kwargs contain the orderby (which is a valid case),
    an empty orderby is returned.

    :param method: the method called.
    :param args: the arguments passed through rpc.
    :param kargs: the keyword arguments passed through rpc.
    :return: the given orderby.
    """
    argument_name = ORDERBY_ARGUMENT_NAMES[method]
    argument_index = ORDERBY_ARGUMENT_INDEXES[method]

    args = args or []
    kwargs = kwargs or {}

    if len(args) > argument_index:
        return args[argument_index]

    return kwargs.get(argument_name) or None


def _parse_fields_from_orderby_clause(order_clause: str):
    parts = order_clause.split(',')
    return [p.split(' ')[0] for p in parts]


def _filter_unauthorized_fields(model: str, record_values: Iterable[dict]):
    """Filter unauthorized fields from the given record values."""
    env = request.env
    if env.user.has_private_data_access():
        return record_values

    private_fields = env['ir.private.field'].get_model_private_fields(model)

    def without_private_fields(r):
        return {k: v for k, v in r.items() if k not in private_fields}

    return [without_private_fields(r) for r in record_values]


def _extract_groupby_from_args_and_kwargs(args: list, kwargs: dict):
    groupby = args[2] if len(args) > 2 else kwargs.get('groupby', [])
    groupby_fields = [groupby] if isinstance(groupby, str) else groupby
    return [f.split(':')[0] for f in groupby_fields]


class DataSetWithPrivateFields(DataSet):
    """Add access restriction to private fields."""

    def do_search_read(
        self, model, fields=False, offset=0, limit=False, domain=None, sort=None
    ):
        fields_to_check = set()

        if sort:
            fields_to_check.update(_parse_fields_from_orderby_clause(sort))

        if domain:
            fields_to_check.update(extract_fields_from_domain(domain))

        check_model_fields_access(model, fields_to_check)

        res = super().do_search_read(
            model, fields=fields, offset=offset, limit=limit, domain=domain, sort=sort
        )
        res['records'] = _filter_unauthorized_fields(model, res['records'])
        return res

    def _call_kw(self, model, method, args, kwargs):
        fields_to_check = set()

        if method == 'read_group':
            fields_to_check.update(_extract_groupby_from_args_and_kwargs(args, kwargs))

        if method in METHODS_WITH_ORDERBY:
            orderby = _get_orderby_from_args_and_kwargs(method, args, kwargs)
            if orderby:
                fields_to_check.update(_parse_fields_from_orderby_clause(orderby))

        if method in SEARCH_METHODS:
            domain = get_domain_from_args_and_kwargs(method, args, kwargs)
            if domain:
                fields_to_check.update(extract_fields_from_domain(domain))

        check_model_fields_access(model, fields_to_check)

        res = super()._call_kw(model, method, args, kwargs)

        if method in ('read', 'search_read'):
            res = _filter_unauthorized_fields(model, res)

        return res
