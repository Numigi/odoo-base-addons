# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import collections
import collections.abc


from odoo.http import HttpDispatcher, SessionExpiredException, root
from werkzeug.exceptions import (
    HTTPException,
    BadRequest,
    Forbidden,
    InternalServerError,
)

from odoo.exceptions import UserError, AccessError, AccessDenied


SESSION_LIFETIME = 60 * 60 * 24 * 7


class HttpDispatcherExtended(HttpDispatcher):
    def handle_error(self, exc: Exception) -> collections.abc.Callable:
        """
        Handle any exception that occurred while dispatching a request
        to a `type='http'` route. Also handle exceptions that occurred
        when no route matched the request path, when no fallback page
        could be delivered and that the request ``Content-Type`` was not
        json.

        :param Exception exc: the exception that occurred.
        :returns: a WSGI application
        """
        if isinstance(exc, SessionExpiredException):
            session = self.request.session
            was_connected = session.uid is not None
            session.logout(keep_db=True)
            response = self.request.redirect_query("/web/login")
            if was_connected:
                root.session_store.rotate(session, self.request.env)
                response.set_cookie(
                    "session_id", session.sid, max_age=SESSION_LIFETIME, httponly=True
                )
            return response

        return (
            exc
            if isinstance(exc, HTTPException)
            else Forbidden(exc.args[0])
            if isinstance(exc, (AccessDenied, AccessError))
            else BadRequest(exc.args[0])
            if isinstance(exc, UserError)
            else InternalServerError()  # hide the real error
        )
