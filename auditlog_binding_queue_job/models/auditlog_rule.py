# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models
import logging

_logger = logging.getLogger(__name__)


class AuditlogRule(models.Model):
    _inherit = "auditlog.rule"

    def create_logs(
        self,
        uid,
        res_model,
        res_ids,
        method,
        old_values=None,
        new_values=None,
        additional_log_values=None,
    ):
        """
        Create logs unless the current request is '/queue_job/runjob'.

        This method skips log creation for queue job execution requests
        to avoid unnecessary logging.
        """
        http_request_model = self.env["auditlog.http.request"]
        current_request_id = None

        try:
            current_request_id = http_request_model.current_http_request()
        except Exception as e:
            _logger.warning(f"Failed to fetch current HTTP request: {e}")
        current_request = False
        if current_request_id:
            current_request = http_request_model.browse(current_request_id)
        if current_request and current_request.name == "/queue_job/runjob":
            return

        return super(AuditlogRule, self).create_logs(
            uid,
            res_model,
            res_ids,
            method,
            old_values=old_values,
            new_values=new_values,
            additional_log_values=additional_log_values,
        )
