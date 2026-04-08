# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import fields
from odoo.addons.web.controllers.dataset import DataSet
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class DataSetWithExtendedSecurity(DataSet):

    def _inject_security_context(self, kwargs):
        """
        Inject the security markers directly into the RPC kwargs.
        This is mandatory because Odoo's native call_kw and call_button
        use .with_context(kwargs.get('context', {})) which completely REPLACES
        the environment context, destroying our markers if they are only in request.env.
        """
        # 1. On force l'injection directement dans le dictionnaire venu du navigateur
        ctx = kwargs.get("context", {})
        ctx["extended_security_enforcement"] = True
        ctx["extended_security_uid"] = request.env.uid
        kwargs["context"] = ctx

        # 2. Mise à jour de l'environnement global pour garantir la couverture
        if hasattr(request, "update_context"):
            request.update_context(**ctx)
        else:
            request.env = request.env(context=dict(request.env.context, **ctx))

    def call_kw(self, model, method, args, kwargs, **kw):
        """Intercept RPC calls to validate Extended Security before and after execution."""
        self._inject_security_context(kwargs)
        _logger.info("Extended Security: Context injected for %s.%s (call_kw)", model, method)

        verifier = _ExtendedSecurityVerifier(model, method, args, kwargs)
        verifier.run_pre_request_checks()
        result = super().call_kw(model, method, args, kwargs, **kw)
        verifier.set_request_result(result)
        verifier.run_post_request_checks()
        return result

    def call_button(self, model, method, args, kwargs, **kw):
        """ Intercept RPC button calls to validate Extended Security before and after execution. """
        self._inject_security_context(kwargs)
        _logger.info("Extended Security: Context injected for %s.%s (call_button)", model, method)

        verifier = _ExtendedSecurityVerifier(model, method, args, kwargs)
        verifier.run_pre_request_checks()
        result = super().call_button(model, method, args, kwargs, **kw)
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
            self._record_ids = args[0] if args else []
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
        if self._method == "create":
            self._record_ids = result

        elif self._method == "name_create":
            self._record_ids = result[0] if result else None

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
        return self._method == "read" and not self._is_many2many_tag_read_request()

    def _is_write(self):
        return self._method in ("write", "toggle_active")

    def _is_create(self):
        return self._method in ("create", "name_create")

    def _is_unlink(self):
        return self._method == "unlink"

    def _is_many2many_tag_read_request(self):
        if self._method != "read":
            return False

        fields_list = set(self._get_read_request_fields() or [])

        all_fields_requested = not fields_list
        if all_fields_requested:
            return False

        has_only_many2many_tag_fields = not fields_list.difference({"display_name", "color"})
        return has_only_many2many_tag_fields

    def _get_read_request_fields(self):
        fields_args_index = 1
        return (
            self._args[fields_args_index]
            if len(self._args) > fields_args_index
            else self._kwargs.get("fields")
        )

    @property
    def _utc_now(self):
        cr = request.env.cr
        cr.execute("SELECT (now() at time zone 'UTC')")
        string_timestamp = cr.fetchone()[0]
        return fields.Datetime.from_string(string_timestamp)

    def _check_read(self):
        _check_read_rules(self._model, self._record_ids)

    def _check_write(self):
        _logger.info("Extended Security: Verifying WRITE access on model '%s' "
                     "for records %s", self._model, self._record_ids)
        _check_write_rules(self._model, self._record_ids)

    def _check_create(self):
        _logger.info("Extended Security: Verifying CREATE access on model '%s'"
                     " for records %s", self._model, self._record_ids)
        _check_create_rules(self._model, self._record_ids)

    def _check_unlink(self):
        _logger.info("Extended Security: Verifying UNLINK access on model '%s'"
                     " for records %s", self._model, self._record_ids)
        _check_unlink_rules(self._model, self._record_ids)

    def _check_x2many_write(self):
        for key, value in self._iter_x2many_list_vals():
            related_model = self._get_related_model(key)
            self._check_x2many_write_for_relation(related_model, value)

    def _check_x2many_write_for_relation(self, related_model, command_list):
        edited_ids = [command[1] for command in command_list if command[0] == 1]
        if edited_ids:
            _logger.info("Extended Security: Verifying X2MANY WRITE access on related "
                         "model '%s' for records %s",
                         related_model, edited_ids)
            _check_write_rules(related_model, edited_ids)

    def _check_x2many_unlink(self):
        for key, value in self._iter_x2many_list_vals():
            related_model = self._get_related_model(key)
            self._check_x2many_unlink_for_relation(related_model, value)

    def _check_x2many_unlink_for_relation(self, related_model, command_list):
        deleted_ids = [command[1] for command in command_list if command[0] == 2]
        existing_deleted_ids = _browse_records(related_model, deleted_ids).exists().ids
        if existing_deleted_ids:
            _logger.info("Extended Security: Verifying X2MANY UNLINK access on related "
                         "model '%s' for records %s",
                         related_model, existing_deleted_ids)
            _check_unlink_rules(related_model, existing_deleted_ids)

    def _check_x2many_create(self):
        for key, _ in self._iter_x2many_list_vals():
            self._check_x2many_create_for_relation(key)

    def _check_x2many_create_for_relation(self, relation_name):
        parent_records = _browse_records(self._model, self._record_ids)
        child_records = parent_records.mapped(relation_name)
        created_child_records = child_records.filtered(
            lambda c: c.create_date == self._utc_now
        )
        if created_child_records:
            _logger.info("Extended Security: Verifying X2MANY CREATE access on related"
                         " model '%s' for records %s",
                         created_child_records._name, created_child_records.ids)
            _check_write_rules(created_child_records._name, created_child_records.ids)

    def _iter_x2many_list_vals(self):
        return (
            (k, v)
            for k, v in self._write_vals.items()
            if _is_x2many_field(self._model, k) and isinstance(v, list)
        )

    @property
    def _write_vals(self):
        if len(self._args) >= 2:
            return self._args[1]
        else:
            return self._kwargs.get("vals") or {}

    def _get_related_model(self, relation_name):
        field = _get_field(self._model, relation_name)
        comodel_name = field.comodel_name
        if not comodel_name:
            raise ValidationError(
                "Field {} of model {} is not a relational field.".format(
                    field, self._model
                )
            )
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
    return field and field.type in ("many2many", "one2many")


def _get_field(model, field_name):
    model_cls = request.env[model]
    return model_cls._fields.get(field_name)