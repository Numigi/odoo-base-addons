# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class File(models.Model):
    _inherit = "dms.file"

    content = fields.Binary(
        required=True,
    )
    type = fields.Selection(
        [("url", "URL"), ("binary", "File")],
        string="Attachment Type",
        default="binary",
    )

    url = fields.Char(string="URL", index=True, size=1024)

    def _create_model_attachment(self, vals):
        res_vals = vals.copy()
        directory = False
        directory_model = self.env["dms.directory"]
        if "directory_id" in res_vals:
            directory = directory_model.browse(res_vals["directory_id"])
        elif self.env.context.get("active_id"):
            directory = directory_model.browse(
                self.env.context.get("active_id"))
        elif self.env.context.get("default_directory_id"):
            directory = directory_model.browse(
                self.env.context.get("default_directory_id")
            )
        if (
                directory
                and directory.res_model
                and directory.res_id
                and directory.storage_id.save_type == "attachment"
        ):
            attachment_vals = {
                "name": vals["name"],
                "datas": vals["content"],
                "res_model": directory.res_model,
                "res_id": directory.res_id,
                "type": vals["type"],
            }
            if vals["type"] == "binary":
                attachment_vals["datas"] = vals["content"]
            else:
                attachment_vals["url"] = vals["url"]
            attachment = (
                self.env["ir.attachment"]
                .with_context(dms_file=True)
                .create(attachment_vals)
            )
            res_vals["attachment_id"] = attachment.id
            res_vals["res_model"] = attachment.res_model
            res_vals["res_id"] = attachment.res_id
            del res_vals["content"]
        return res_vals
