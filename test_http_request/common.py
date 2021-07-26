# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import werkzeug
from contextlib import contextmanager
from io import BytesIO
from odoo.addons.http_routing.models.ir_http import url_for
from odoo.api import Environment
from odoo.http import HttpRequest, JsonRequest, OpenERPSession, _request_stack
from odoo.tools import config
from typing import Optional, Union
from werkzeug.contrib.sessions import FilesystemSessionStore, Session
from werkzeug.datastructures import ImmutableOrderedMultiDict
from werkzeug.test import EnvironBuilder
from werkzeug.urls import url_encode
from werkzeug.wrappers import Request


class _MockOdooRequestMixin:

    @staticmethod
    def redirect(url, code=302):
        """Add the `redirect` method to the request.

        This method is added programatically by the module http_routing:
            odoo/addons/http_routing/models/ir_http.py (method _dispatch)
        """
        return werkzeug.utils.redirect(url_for(url), code)

    @property
    def website(self):
        """Add the `website` property to the request.

        The attribute is added programatically by the module website:
            odoo/addons/website/models/ir_http.py (method _add_dispatch_parameters)

        The attribute is added as a property so that the request object
        can be used even if the module website is not installed.
        """
        return self.env['website'].get_current_website()

    def __exit__(self, exc_type, exc_value, traceback):
        """Prevent commiting the transaction when exiting the HTTP request.

        Since the request uses the same cursor as the test fixture,
        the cursor must not be commited when exiting the request.
        """
        _request_stack.pop()


class _MockOdooHttpRequest(_MockOdooRequestMixin, HttpRequest):
    pass


class _MockOdooJsonRequest(_MockOdooRequestMixin, JsonRequest):
    pass


def _make_environ_form_data_stream(data: dict) -> BytesIO:
    """Make the form data stream for an Odoo http request.

    Odoo uses ImmutableOrderedMultiDict to store url encoded form
    data instead of the default ImmutableMultiDict in werkzeug.

    The test utility :class:`werkzeug.test.EnvironBuilder` uses
    MultiDict to store form data.

    This must be ajusted in order reproduce properly the behavior of Odoo.
    """
    encoded_data = url_encode(data).encode("ascii")
    return BytesIO(encoded_data)


def _make_environ(
    method: str = 'POST',
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    routing_type: str = 'http',
):
    """Make an environ for the given request parameters."""
    assert routing_type in ('http', 'json')

    environ_builder = EnvironBuilder(
        method=method,
        data=json.dumps(data or {}) if routing_type == 'json' else data,
        headers=headers,
        content_type=_get_content_type(headers, routing_type),
    )
    environ = environ_builder.get_environ()

    if routing_type == 'http' and data:
        environ['wsgi.input'] = _make_environ_form_data_stream(data)

    return environ


def _get_content_type(headers, routing_type):
    content_type = headers.get("Content-Type")

    if not content_type:
        content_type = (
            'application/json' if routing_type == 'json' else
            'application/x-www-form-urlencoded'
        )

    return content_type


def _set_request_storage_class(httprequest: Request):
    """Set the data structure used to store form data.

    This is done in the method Root.dispatch of odoo/http.py.
    """
    httprequest.parameter_storage_class = ImmutableOrderedMultiDict


def _make_werkzeug_request(environ: dict) -> Request:
    """Make a werkzeug request from the given environ."""
    httprequest = Request(environ)
    _set_request_storage_class(httprequest)
    return httprequest


def _make_filesystem_session(env: Environment) -> Session:
    session_store = FilesystemSessionStore(
        config.session_dir, session_class=OpenERPSession, renew_missing=True)
    session = session_store.new()
    session.db = env.cr.dbname
    session.uid = env.uid
    session.context = env.context
    return session


def _make_odoo_request(
        werkzeug_request: Request, env: Environment, routing_type: str,
) -> Union[_MockOdooHttpRequest, _MockOdooJsonRequest]:
    """Make an Odoo request from the given werkzeug request."""
    odoo_request_cls = (
        _MockOdooJsonRequest if routing_type == 'json' else
        _MockOdooHttpRequest
    )
    odoo_request = odoo_request_cls(werkzeug_request)
    odoo_request._env = env
    odoo_request._cr = env.cr
    odoo_request._uid = env.uid
    odoo_request._context = env.context
    return odoo_request


@contextmanager
def mock_odoo_request(
    env: Environment,
    method: str = 'POST',
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    routing_type: str = 'http',
):
    """Mock an Odoo HTTP request.

    This methods builds an HttpRequest object and adds it to
    the local stack of the application.

    The Odoo environment of the test fixture is injected to the
    request so that objects created in the fixture are available
    for controllers.

    :param env: the odoo environment to bind with the request.
    :param method: the HTTP method called during the request.
    :param headers: the request headers.
    :param data: an optional dict to be serialized as json or url-encoded data.
    :param routing_type: whether to use an http (x-www-form-urlencoded) or json request.
    """
    environ = _make_environ(method, headers, data, routing_type)
    werkzeug_request = _make_werkzeug_request(environ)
    werkzeug_request.session = _make_filesystem_session(env)
    odoo_request = _make_odoo_request(werkzeug_request, env, routing_type)

    with odoo_request:
        yield odoo_request
