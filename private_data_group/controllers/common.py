# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _
from odoo.exceptions import AccessError, ValidationError
from odoo.http import request
from typing import Iterable, List


def _get_related_model(model: str, relation: str):
    model_cls = request.env[model]

    if relation not in model_cls._fields:
        raise ValidationError('Model {} has no field {}.'.format(model, relation))

    comodel_name = model_cls._fields[relation].comodel_name
    if not comodel_name:
        raise ValidationError(
            'Field {} of model {} is not a relational field.'.format(relation, model))

    return comodel_name


def _raise_private_field_access_error(model: str, field: str):
    raise AccessError(
        _('You do not have access to the field {field} of model {model}')
        .format(field=field, model=model)
    )


def check_model_fields_access(model: str, fields: Iterable[str]):
    env = request.env
    if env.user.has_private_data_access():
        return

    fields = [f for f in fields if isinstance(f, str)]

    related_model_fields = (f for f in fields if '.' in f)
    for field in related_model_fields:
        relation, dummy, remaining_field_parts = field.partition('.')
        related_model = _get_related_model(model, relation)
        check_model_fields_access(related_model, [remaining_field_parts])

    private_fields = env['ir.private.field'].get_model_private_fields(model)
    for field in fields:
        column_name = field.split('.')[0].split(':')[0]
        if column_name in private_fields:
            _raise_private_field_access_error(model, field)


def extract_fields_from_domain(domain: List):
    field_tuples = [e for e in domain if isinstance(e, (list, tuple))]
    return [t[0] for t in field_tuples]
