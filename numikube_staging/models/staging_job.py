# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from datetime import datetime
from urllib.parse import urljoin

import requests
from odoo import fields, models, api, _
from odoo.exceptions import AccessError, ValidationError

FIELD_STATES = {"done": [("readonly", True)]}


class StagingJob(models.Model):
    _name = "staging.job"
    _description = "Staging Job"
    _order = "start_datetime desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    environment_id = fields.Many2one(
        "staging.environment",
        required=True,
        states=FIELD_STATES,
        tracking=True,
        default=lambda self: self._get_default_staging_environment()
    )
    type_ = fields.Selection(
        [
            ("prod2x", "New Database"),
            ("dropdb", "Drop Databases"),
        ],
        default="prod2x",
        required=True,
        states=FIELD_STATES,
    )
    dropdb_database_names = fields.Text(states=FIELD_STATES)
    suffix = fields.Char(
        states=FIELD_STATES,
        tracking=True,
    )
    timestamp = fields.Boolean(
        states=FIELD_STATES,
        tracking=True,
        default=True,
    )
    error = fields.Char(
        readonly=True,
        tracking=True,
        copy=False,
    )
    traceback = fields.Text(
        readonly=True,
        copy=False,
    )
    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("running", "Running"),
            ("done", "Done"),
            ("error", "Error"),
        ],
        "Status",
        required=True,
        readonly=True,
        default="pending",
        tracking=True,
    )
    start_datetime = fields.Datetime(
        "Start Time",
        readonly=True,
        tracking=True,
        copy=False,
    )
    database_name = fields.Char(readonly=True, copy=False)
    user_id = fields.Many2one(
        "res.users",
        ondelete="restrict",
        default=lambda self: self.env.user,
    )
    partner_id = fields.Many2one(related="user_id.partner_id")

    def _get_default_staging_environment(self):
        staging_env = self.env["staging.environment"].search([])
        if len(staging_env) == 1:
            return staging_env

    def name_get(self):
        return [(r.id, r._get_display_name()) for r in self]

    def _get_display_name(self):
        return self.database_name or _("New Staging Job")

    @api.constrains("suffix")
    def _check_suffix(self):
        pattern = r'^[a-z0-9_]+(?:-[a-z0-9_]+)*$'
        for job in self:
            if job.suffix and not re.match(pattern, job.suffix):
                raise ValidationError(
                    _(
                        "The suffix should not contain any spaces,"
                        "special characters, or uppercase letters"
                    )
                )

    def run(self):
        self.start_datetime = datetime.now()

        response = self._call_webhook()
        if response.status_code == 200:
            self._parse_success_response(response)
        else:
            self._parse_error_response(response)

    def run_callback(self, data):
        self._check_callback_token(data)
        self.state = data.get("state") or "error"
        self.error = data.get("error")
        self.traceback = data.get("traceback")

        if self.state == "done":
            self._send_message_done()
        else:
            self._send_message_failed()

    def _send_message_done(self):
        template = self.env.ref("numikube_staging.staging_job_done_template")
        self.message_post_with_template(template.id)

    def _send_message_failed(self):
        template = self.env.ref("numikube_staging.staging_job_failed_template")
        self.message_post_with_template(template.id)

    def _check_callback_token(self, data):
        expected = self.environment_id.token
        if expected != data.get("token"):
            raise AccessError("Wrong given staging token")

    def _parse_success_response(self, response):
        data = response.json()
        error = data.get("error")

        if error:
            self._handle_odoo_error_response(error)

        elif self.type_ == "dropdb":
            self._handle_dropdb_success()

        else:
            self._handle_prod2x_running(data)

    def _handle_prod2x_running(self, data):
        self.state = "running"
        self.error = False
        self.traceback = False
        self.database_name = data["result"].get("db_name")

    def _handle_dropdb_success(self):
        self.state = "done"
        self.error = False
        self.traceback = False

    def _handle_odoo_error_response(self, error):
        self.state = "error"
        self.error = error["data"]["message"]
        self.traceback = _format_traceback(error["data"]["debug"])

    def _parse_error_response(self, response):
        self.state = "error"
        self.error = response.text
        self.traceback = False

    def _call_webhook(self):
        url = self._get_webhook_url()
        data = self._get_webhook_data()
        return requests.post(url, json=data)

    def _get_webhook_data(self):
        data = self._get_webhook_data_common()

        if self.type_ == "prod2x":
            data["level"] = self.environment_id.level
            data["suffix"] = self.suffix

        elif self.type_ == "dropdb":
            data["database_names"] = self.dropdb_database_names

        return data

    def _get_webhook_data_common(self):
        return {
            "token": self.environment_id.token,
            "client": self.environment_id.client,
            "type": self.type_,
            "timestamp": self.timestamp,
            "callback": self._get_callback_url(),
        }

    def _get_webhook_url(self):
        return urljoin(self.environment_id.url, "/web/staging/run")

    def _get_callback_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")

        if not base_url:
            raise ValidationError(
                _(
                    "Can not run a staging because the web.base.url parameter "
                    "is not defined on the local instance."
                )
            )

        return urljoin(base_url, f"/web/staging/callback/{self.id}")


def _format_traceback(traceback):
    return traceback.replace("\\n", "\n")
