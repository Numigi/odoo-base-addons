# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.web.controllers.main import DataSet
from odoo.http import request


class DataSetWithExtendedSecurity(DataSet):
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
