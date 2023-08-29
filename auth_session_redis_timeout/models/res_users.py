# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging


from odoo import models, http, api
from odoo.http import SessionExpiredException

_logger = logging.getLogger(__name__)



class ResUsers(models.Model):
    _inherit = 'res.users'


    @api.model_cr_context
    def _auth_timeout_check(self):
        """Perform session timeout validation and expire if needed."""

        if not http.request:
            return

        session = http.request.session
        session_store = http.Root().session_store

        # Calculate deadline
        deadline = self._auth_timeout_deadline_calculate()

        # Check if past deadline
        expired = False
        if deadline is not False:            
            time = session_store.get_activity_time(session)
            try:
                expired = time < deadline
            except OSError:
                _logger.exception(
                    'Exception reading redis session',
                )
                # Force expire the session. Will be resolved with new session.
                expired = True

        # Try to terminate the session
        terminated = False
        if expired:
            terminated = self._auth_timeout_session_terminate(session)

        # If session terminated, all done
        if terminated:
            session_store.delete(session)
            raise SessionExpiredException("Session expired")

        # Else, conditionally update session modified and access times
        ignored_urls = self._auth_timeout_get_ignored_urls()

        if http.request.httprequest.path not in ignored_urls:
            try:
                # Enregistrer la date de modification
                session_store.set_activity_time(session)
            except OSError:
                _logger.exception(
                    'Exception updating redis session updated_at.',
                )

