# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import json

from google.oauth2 import service_account
from odoo.exceptions import UserError
from odoo import api, fields, models, _


class GoogleAppConf(models.Model):
    _name = "google.application"
    _description = "Google Application"

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Application name", required=True, copy=False)
    project_id = fields.Char(string="Project name", required=True, copy=False)
    auth_type = fields.Selection(
        [("service_account", "Service Account")],
        string="Authentication Type",
        required=True,
        default="service_account",
    )
    filename = fields.Char("File Name")
    json_file = fields.Binary(attachment=True)
    scope = fields.Char(string="Scope", required=True, copy=False)

    @api.model
    def google_api_auth(self):
        self.ensure_one()
        try:
            info = json.loads(
                base64.b64decode(self.json_file).decode("utf-8")
            )
            creds = service_account.Credentials.from_service_account_info(
                info, scopes=[self.scope]
            )

            return creds
        except Exception as error:
            UserError(_("Authentication Test Failed! \n %s" % error))

    def test_google_api_auth(self):
        for app in self:
            try:
                app.google_api_auth()
            except UserError as error:
                raise error
            title = _("Authentication Test Succeeded!")
            message = _("Everything seems properly set up!")
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": title,
                    "message": message,
                    "sticky": False,
                },
            }
