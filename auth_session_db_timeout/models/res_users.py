# Copyright 2025 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import os
import logging

from odoo import api, http, models
from odoo.http import SessionExpiredException

from ..utils.pg_session_store import PGSessionStoreExtended

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"

    @api.model
    def _auth_timeout_check(self):
        """
        !!! Important !!!
        This is the function where we call
        functions that retrieve
        session data from the filestore.
        """

        session_db_uri = os.environ.get("SESSION_DB_URI")
        custom_session_store = PGSessionStoreExtended(
            session_db_uri,
            session_class=http.OpenERPSession
        )

        if not http.request:
            return

        session = http.request.session

        # Calculate deadline
        deadline = self._auth_timeout_deadline_calculate()

        # Check if past deadline
        expired = False
        if deadline is not False:

            try:
                write_date = custom_session_store.get_write_date(session.sid)
                expired = write_date.timestamp() < deadline
            except Exception as e:
                _logger.exception(
                    f"Exception session data modified time in database. {e}",
                )
                # Force expire the session. Will be resolved with new session.
                expired = True

        # Try to terminate the session
        terminated = False
        if expired:
            terminated = self._auth_timeout_session_terminate(session)

        # If session terminated, all done
        if terminated:
            raise SessionExpiredException("Session expired")

        # Else, conditionally update session modified and access times
        ignored_urls = self._auth_timeout_get_ignored_urls()

        if http.request.httprequest.path not in ignored_urls:
            try:
                custom_session_store.save(session)
            except Exception as e:
                _logger.exception(
                    f"Exception updating session in database htt_sessions. {e}",
                )
