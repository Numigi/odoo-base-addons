# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import werkzeug
import contextvars
from contextlib import contextmanager
from io import BytesIO
from urllib.parse import urlencode

import odoo.http
from odoo.api import Environment
from odoo.http import (
    Request as OdooRequest,
    Session,
    Response,
)
from typing import Optional
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers.request import Request as WerkzeugRequest


class _MockOdooRequest(OdooRequest):
    @staticmethod
    def redirect(url, code=302):
        return werkzeug.utils.redirect(url, code)

    @property
    def website(self):
        return self.env["website"].get_current_website()

    def __enter__(self):
        self._cv_obj = None
        self._cv_token = None

        # 1. Fallback pour les anciennes versions (Odoo <= 16)
        if hasattr(odoo.http, '_request_stack') and hasattr(odoo.http._request_stack, 'push'):
            odoo.http._request_stack.push(self)
            return self

        # 2. Odoo 17/18 avec Werkzeug 3.0 : on détecte le ContextVar dynamiquement
        for name, obj in vars(odoo.http).items():
            if isinstance(obj, contextvars.ContextVar) and 'request' in name.lower():
                self._cv_obj = obj
                self._cv_token = obj.set(self)
                return self

        # 3. Fallback ultime si la structure interne a encore changé
        self._original_request = getattr(odoo.http, 'request', None)
        odoo.http.request = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(odoo.http, '_request_stack') and hasattr(odoo.http._request_stack, 'pop'):
            odoo.http._request_stack.pop()
        elif self._cv_obj and self._cv_token:
            self._cv_obj.reset(self._cv_token)
        elif hasattr(self, '_original_request'):
            odoo.http.request = self._original_request

    def make_response(self, data, headers=None, cookies=None, status=200):
        response = Response(data, status=status, headers=headers)
        if cookies:
            for k, v in cookies.items():
                response.set_cookie(k, v)
        return response


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


def _set_request_storage_class(httprequest: WerkzeugRequest):
    httprequest.parameter_storage_class = ImmutableMultiDict


def _make_werkzeug_request(environ: dict) -> WerkzeugRequest:
    httprequest = WerkzeugRequest(environ)
    _set_request_storage_class(httprequest)
    return httprequest


def _make_filesystem_session(env: Environment) -> Session:
    session = Session({}, "mock_session_id")
    session.db = env.cr.dbname
    session.uid = env.uid
    session.context = env.context
    return session


def _make_odoo_request(
        werkzeug_request: WerkzeugRequest, env: Environment, routing_type: str
) -> _MockOdooRequest:
    odoo_request = _MockOdooRequest(werkzeug_request)

    # Sécurisation contre le blocage de modification du curseur en V18
    try:
        odoo_request.env = env
    except Exception:
        pass

    odoo_request._env = env
    odoo_request.registry = env.registry
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