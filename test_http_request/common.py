# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
import werkzeug
from contextlib import contextmanager
from odoo.addons.http_routing.models.ir_http import url_for
from odoo.api import Environment
from odoo.http import HttpRequest, JsonRequest, OpenERPSession, _request_stack
from odoo.tools import config
from typing import Optional
from werkzeug.contrib.sessions import FilesystemSessionStore
from werkzeug.test import EnvironBuilder
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
    )
    environ_builder.content_type = (
        'application/json' if routing_type == 'json' else
        'application/x-www-form-urlencoded'
    )
    environ = environ_builder.get_environ()
    return environ


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
    :param routing_type: whether to send an http (x-www-form-urlencoded) or json request.
    """
    environ = _make_environ(method, headers, data, routing_type)
    httprequest = Request(environ)

    session_store = FilesystemSessionStore(
        config.session_dir, session_class=OpenERPSession, renew_missing=True)
    session = session_store.new()
    session.db = env.cr.dbname
    session.uid = env.uid
    session.context = env.context

    httprequest.session = session

    odoo_http_request_cls = (
        _MockOdooJsonRequest if routing_type == 'json' else
        _MockOdooHttpRequest
    )
    odoo_http_request = odoo_http_request_cls(httprequest)
    odoo_http_request._env = env
    odoo_http_request._cr = env.cr
    odoo_http_request._uid = env.uid
    odoo_http_request._context = env.context

    with odoo_http_request:
        yield odoo_http_request
