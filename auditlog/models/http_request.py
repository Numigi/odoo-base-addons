# © 2015 ABF OSIELL <https://osiell.com>
# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.http import request


class AuditlogHTTPRequest(models.Model):

    _name = 'auditlog.http.request'
    _description = "Auditlog - HTTP request log"
    _order = "create_date DESC"

    display_name = fields.Char("Name", compute="_compute_display_name", store=True)
    name = fields.Char("Path")
    root_url = fields.Char("Root URL")
    user_id = fields.Many2one('res.users', string="User")
    user_context = fields.Char("Context")
    log_ids = fields.One2many('auditlog.log', 'http_request_id', string="Logs")

    @api.depends('create_date', 'name')
    def _compute_display_name(self):
        for http_request in self:
            create_date = fields.Datetime.from_string(http_request.create_date)
            tz_create_date = fields.Datetime.context_timestamp(http_request, create_date)
            http_request.display_name = "{name} ({create_date})".format(
                name=http_request.name or '?',
                create_date=fields.Datetime.to_string(tz_create_date)
            )

    
    def name_get(self):
        return [(request.id, request.display_name) for request in self]

    @api.model
    def current_http_request(self):
        """Get a record representing the current http request.

        This method can be called several times during the
        HTTP query/response cycle, it will only log the request on the first call.

        If no HTTP request is available, returns an empty recordset.
        """
        if not request or not request.httprequest:
            return self

        record = self._get_http_request_record(request.httprequest)
        request.httprequest.auditlog_http_request_id = record.id
        return record

    @api.model
    def _get_http_request_record(self, http_request):
        record = self._find_existing_http_request_record(http_request)

        if record is None:
            record = self._create_http_request_record(http_request)

        return record

    @api.model
    def _create_http_request_record(self, http_request):
        vals = {
            'name': http_request.path,
            'root_url': http_request.url_root,
            'user_id': request.uid,
            'user_context': request.context,
        }
        return self.create(vals)

    @api.model
    def _find_existing_http_request_record(self, http_request):
        """Find an existing http request record.

        The database id of the record is stored in auditlog_http_request_id.

        We check that the record exists because it may have been rolled back
        ater a concurrency error.
        """
        if hasattr(http_request, 'auditlog_http_request_id'):
            record = self.browse(http_request.auditlog_http_request_id)
            return record if record.exists() else None
        else:
            return None
