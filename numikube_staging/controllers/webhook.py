# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.addons.numikube_staging.staging import run_staging_job
from odoo.addons.numikube_staging.callback import run_callback


class StagingWebhook(http.Controller):
    @http.route("/web/staging/run", type="json", auth="none", csrf=False)
    def staging_run(self, **kwargs):
        data = http.request.jsonrequest
        return run_staging_job(data)

    @http.route(
        "/web/staging/callback/<int:job_id>", type="json", auth="none", csrf=False
    )
    def staging_callback(self, job_id, **kwargs):
        data = http.request.jsonrequest
        return run_callback(http.request.env, job_id, data)
