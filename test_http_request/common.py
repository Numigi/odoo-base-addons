# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import werkzeug
from contextlib import contextmanager
from io import BytesIO
from urllib.parse import urlencode

import odoo.http
from odoo.api import Environment
from odoo.http import (
    HttpRequest,
    JsonRequest,
    Session,
    Response,
)
from typing import Optional, Union
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers.request import Request


class _MockOdooRequestMixin:
    @staticmethod
    def redirect(url, code=302):
        return werkzeug.utils.redirect(url, code)

    @property
    def website(self):
        return self.env["website"].get_current_website()

    def __exit__(self, exc_type, exc_value, traceback):
        # Odoo 18: On restaure la requête précédente via les contextvars
        odoo.http.request_ctx.reset(self._previous_request)

    def __enter__(self):
        # Odoo 18: On pousse la requête courante via les contextvars
        self._previous_request = odoo.http.request_ctx.set(self)
        return self

    def make_response(self, data, headers=None, cookies=None, status=200):
        response = Response(data, status=status, headers=headers)
        if cookies:
            for k, v in cookies.items():
                response.set_cookie(k, v)
        return response


class _MockOdooHttpRequest(_MockOdooRequestMixin, HttpRequest):
    pass


class _MockOdooJsonRequest(_MockOdooRequestMixin, JsonRequest):
    pass


def _make_environ_form_data_stream(data: dict) -> BytesIO:
    encoded_data = urlencode(data).encode("ascii")
    return BytesIO(encoded_data)


def _make_environ(
        method: str = "POST",
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        routing_type: str = "http",
):
    assert routing_type in ("http", "json")
    environ_builder = EnvironBuilder(
        method=method,
        data=json.dumps(data or {}) if routing_type == "json" else data,
        headers=headers,
        content_type=(
            "application/json"
            if routing_type == "json"
            else "application/x-www-form-urlencoded"
        ),
    )
    environ = environ_builder.get_environ()

    if routing_type == "http" and data:
        environ["wsgi.input"] = _make_environ_form_data_stream(data)
    return environ


def _set_request_storage_class(httprequest: Request):
    # Odoo 18: ImmutableOrderedMultiDict n'existe plus dans Werkzeug 3.0
    httprequest.parameter_storage_class = ImmutableMultiDict


def _make_werkzeug_request(environ: dict) -> Request:
    httprequest = Request(environ)
    _set_request_storage_class(httprequest)
    return httprequest


def _make_filesystem_session(env: Environment) -> Session:
    # Odoo 18: FilesystemSessionStore a été remplacé par une gestion unifiée
    session = Session()
    session.db = env.cr.dbname
    session.uid = env.uid
    session.context = env.context
    return session


def _make_odoo_request(
        werkzeug_request: Request, env: Environment, routing_type: str
) -> Union[_MockOdooHttpRequest, _MockOdooJsonRequest]:
    odoo_request_cls = (
        _MockOdooJsonRequest if routing_type == "json" else _MockOdooHttpRequest
    )
    odoo_request = odoo_request_cls(werkzeug_request)

    # Assure la compatibilité avec la manière dont Odoo gère les propriétés d'environnement
    try:
        odoo_request.env = env
    except AttributeError:
        pass
    odoo_request._env = env
    odoo_request._cr = env.cr
    odoo_request._uid = env.uid
    odoo_request._context = env.context
    odoo_request.httprequest = werkzeug_request
    return odoo_request


@contextmanager
def mock_odoo_request(
        env: Environment,
        method: str = "POST",
        headers: Optional[dict] = None,
        data: Optional[dict] = None,
        routing_type: str = "http",
):
    environ = _make_environ(method, headers, data, routing_type)
    werkzeug_request = _make_werkzeug_request(environ)
    werkzeug_request.session = _make_filesystem_session(env)
    odoo_request = _make_odoo_request(werkzeug_request, env, routing_type)

    with odoo_request:
        yield odoo_request
