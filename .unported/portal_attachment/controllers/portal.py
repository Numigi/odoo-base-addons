# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.mail import PortalChatter


class PortalChatterWithAttachments(PortalChatter):
    @http.route(
        ["/mail/chatter_post"],
        type="http",
        methods=["POST"],
        auth="public",
        website=True,
    )
    def portal_chatter_post(self, res_model, res_id, message, **kw):
        kwargs = {k: v for k, v in kw.items() if k != "attachments"}
        _create_attachments(res_model, res_id)
        return super().portal_chatter_post(res_model, res_id, message, **kwargs)


def _create_attachments(res_model, res_id):
    files = request.httprequest.files.getlist("attachments")

    attachments = request.env["ir.attachment"]

    for file in files:
        attachments |= _create_single_attachment(res_model, res_id, file)

    return attachments


def _create_single_attachment(res_model, res_id, file):
    return (
        request.env["ir.attachment"]
        .sudo()
        .create(
            {
                "res_model": res_model,
                "res_id": res_id,
                "name": file.filename,
                "datas": base64.encodestring(file.read()),
                "datas_fname": file.filename,
            }
        )
    )
