# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import requests
from odoo import api, models


class Users(models.Model):

    _inherit = "res.users"

    @api.model
    def _auth_oauth_rpc(self, endpoint, access_token):
        if _is_microsoft_endpoint(endpoint):
            return self._auth_oauth_rpc_microsoft(endpoint, access_token)
        else:
            return super()._auth_oauth_rpc(endpoint, access_token)

    def _auth_oauth_rpc_microsoft(self, endpoint, access_token):
        headers = {"Authorization": "Bearer {}".format(access_token)}
        response = requests.get(endpoint, headers=headers)
        return response.json()

    @api.model
    def _auth_oauth_validate(self, provider, access_token):
        validation = super()._auth_oauth_validate(provider, access_token)

        provider_obj = self.env["auth.oauth.provider"].browse(provider)
        if _is_microsoft_endpoint(provider_obj.auth_endpoint):
            validation["user_id"] = validation.get("email") or validation["sub"]

        return validation


def _is_microsoft_endpoint(endpoint):
    return "microsoft" in endpoint
