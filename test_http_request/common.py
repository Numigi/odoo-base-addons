# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from contextlib import contextmanager
from odoo.api import Environment
from odoo.http import HttpRequest, OpenERPSession
from odoo.tools import config
from werkzeug.contrib.sessions import FilesystemSessionStore
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request


@contextmanager
def mock_odoo_request(env: Environment):
    """Mock an Odoo HTTP request.

    This methods builds an HttpRequest object and adds it to
    the local stack of the application.

    The Odoo environment of the test fixture is injected to the
    request so that objects created in the fixture are available
    for controllers.
    """
    session = FilesystemSessionStore(
        config.session_dir, session_class=OpenERPSession, renew_missing=True)
    session.db = env.cr.dbname
    session.uid = env.uid
    session.context = env.context

    environ_builder = EnvironBuilder(method='POST', data={})
    environ = environ_builder.get_environ()
    httprequest = Request(environ)
    httprequest.session = session

    odoo_http_request = HttpRequest(httprequest)
    odoo_http_request._env = env
    with odoo_http_request:
        yield
