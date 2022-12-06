# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields
from odoo.addons.web.controllers.main import DataSet
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools.func import lazy_property


class DataSetWithExtendedSecurity(DataSet):

    def _call_kw(self, model, method, args, kwargs):
        verifier = _ExtendedSecurityVerifier(model, method, args, kwargs)
        verifier.run_pre_request_checks()
        result = super()._call_kw(model, method, args, kwargs)
        verifier.set_request_result(result)
        verifier.run_post_request_checks()
        return result


class _ExtendedSecurityVerifier:

    def __init__(self, model, method, args, kwargs):
        self._model = model
        self._method = method
        self._args = args
        self._kwargs = kwargs

        if self._is_read() or self._is_write() or self._is_unlink():
            self._record_ids = args[0]
        else:
            self._record_ids = None

    def run_pre_request_checks(self):
        if self._is_read():
            self._check_read()

        elif self._is_write():
            self._check_write()
            self._check_x2many_write()
            self._check_x2many_unlink()

        elif self._is_unlink():
            self._check_unlink()

    def set_request_result(self, result):
        if self._method == 'create':
            self._record_ids = result

        elif self._method == 'name_create':
            self._record_ids = result[0]

    def run_post_request_checks(self):
        if self._is_create():
            self._check_create()
            self._check_x2many_write()
            self._check_x2many_create()

        elif self._is_write():
            self._check_write()
            self._check_x2many_write()
            self._check_x2many_create()

    def _is_read(self):
        return self._method == 'read' and not self._is_many2many_tag_read_request()

    def _is_write(self):
        return self._method in ('write', 'toggle_active')

    def _is_create(self):
        return self._method in ('create', 'name_create')

    def _is_unlink(self):
        return self._method == 'unlink'

    def _is_many2many_tag_read_request(self):
        if self._method != 'read':
            return False

        fields = set(self._get_read_request_fields() or [])

        all_fields_requested = not fields
        if all_fields_requested:
            return False

        has_only_many2many_tag_fields = not fields.difference(('display_name', 'color'))
        return has_only_many2many_tag_fields

    def _get_read_request_fields(self):
        fields_args_index = 1
        return (
            self._args[fields_args_index]
            if len(self._args) > fields_args_index
            else self._kwargs.get('fields')
        )

    @lazy_property
    def _utc_now(self):
        cr = request.env.cr
        cr.execute("SELECT (now() at time zone 'UTC')")
        string_timestamp = cr.fetchone()[0]
        return fields.Datetime.from_string(string_timestamp)

    def _check_read(self):
        _check_read_rules(self._model, self._record_ids)

    def _check_write(self):
        _check_write_rules(self._model, self._record_ids)

    def _check_create(self):
        _check_create_rules(self._model, self._record_ids)

    def _check_unlink(self):
        _check_unlink_rules(self._model, self._record_ids)

    def _check_x2many_write(self):
        for key, value in self._iter_x2many_list_vals():
            related_model = self._get_related_model(key)
            self._check_x2many_write_for_relation(related_model, value)

    def _check_x2many_write_for_relation(self, related_model, command_list):
        edited_ids = [command[1] for command in command_list if command[0] == 1]
        if edited_ids:
            _check_write_rules(related_model, edited_ids)

    def _check_x2many_unlink(self):
        for key, value in self._iter_x2many_list_vals():
            related_model = self._get_related_model(key)
            self._check_x2many_unlink_for_relation(related_model, value)

    def _check_x2many_unlink_for_relation(self, related_model, command_list):
        deleted_ids = [command[1] for command in command_list if command[0] == 2]
        existing_deleted_ids = _browse_records(related_model, deleted_ids).exists().ids
        if existing_deleted_ids:
            _check_unlink_rules(related_model, existing_deleted_ids)

    def _check_x2many_create(self):
        for key, _ in self._iter_x2many_list_vals():
            self._check_x2many_create_for_relation(key)

    def _check_x2many_create_for_relation(self, relation_name):
        parent_records = _browse_records(self._model, self._record_ids)
        child_records = parent_records.mapped(relation_name)
        created_child_records = child_records.filtered(lambda c: c.create_date == self._utc_now)
        if created_child_records:
            _check_write_rules(created_child_records._name, created_child_records.ids)

    def _iter_x2many_list_vals(self):
        return (
            (k, v) for k, v in self._write_vals.items()
            if _is_x2many_field(self._model, k) and isinstance(v, list)
        )

    @lazy_property
    def _write_vals(self):
        if len(self._args) >= 2:
            return self._args[1]
        else:
            return self._kwargs.get('vals') or {}

    def _get_related_model(self, relation_name):
        field = _get_field(self._model, relation_name)
        comodel_name = field.comodel_name
        if not comodel_name:
            raise ValidationError(
                'Field {} of model {} is not a relational field.'.format(field, self._model))
        return comodel_name


def _check_read_rules(model, record_ids):
    records = _browse_records(model, record_ids)
    records.check_extended_security_read()


def _check_write_rules(model, record_ids):
    records = _browse_records(model, record_ids)
    records.check_extended_security_write()


def _check_create_rules(model, record_ids):
    records = _browse_records(model, record_ids)
    records.check_extended_security_create()


def _check_unlink_rules(model, record_ids):
    records = _browse_records(model, record_ids)
    records.check_extended_security_unlink()


def _browse_records(model, record_ids):
    return request.env[model].browse(record_ids)


def _is_x2many_field(model, field_name):
    field = _get_field(model, field_name)
    return field and field.type in ('many2many', 'one2many')


def _get_field(model, field_name):
    model_cls = request.env[model]
    return model_cls._fields.get(field_name)
