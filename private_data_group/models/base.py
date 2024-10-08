# Copyright 2022-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, api
from odoo.http import request
from typing import Iterable
from ..controllers.common import check_model_fields_access, extract_fields_from_domain


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


class BasePrivateDataGroup(models.AbstractModel):

    _inherit = "base"

    @api.model
    def web_search_read(self, domain=None, fields=None, offset=0, limit=None,
                        order=None, count_limit=None):
        """
        Performs a search_read and a search_count.

        :param domain: search domain
        :param fields: list of fields to read
        :param limit: maximum number of records to read
        :param offset: number of records to skip
        :param order: columns to sort results
        :return: {
            'records': array of read records (result of a call to 'search_read')
            'length': number of records matching the domain (result of a call to 'search_count')
        }
        """

        fields_to_check = set()
        if order:
            fields_to_check.update(_parse_fields_from_orderby_clause(order))

        if domain:
            fields_to_check.update(extract_fields_from_domain(domain))
        model = self._context.get('active_model', False)
        check_model_fields_access(model, fields_to_check)
        res = super().web_search_read(
            domain=domain, fields=fields, offset=offset,
            limit=limit, order=order, count_limit=count_limit)
        res['records'] = _filter_unauthorized_fields(model, res['records'])
        return res
