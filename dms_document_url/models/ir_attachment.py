# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _dms_operations(self):
        for attachment in self:
            if (
                    attachment.type not in ("url", "binary")
                    or not attachment.res_model
                    or not attachment.res_id
            ):
                continue
            directories = self._get_dms_directories(
                attachment.res_model, attachment.res_id
            )
            if not directories:
                attachment._dms_directories_create()
                # Get dms_directories again (with items previously created)
                directories = self._get_dms_directories(
                    attachment.res_model, attachment.res_id
                )
            # Auto-create_files (if not exists)
            for directory in directories:
                dms_file_model = self.env["dms.file"].sudo()
                dms_file = dms_file_model.search(
                    [
                        ("attachment_id", "=", attachment.id),
                        ("directory_id", "=", directory.id),
                    ]
                )
                if not dms_file:
                    dms_file_model.create(
                        {
                            "name": attachment.name,
                            "directory_id": directory.id,
                            "attachment_id": attachment.id,
                            "res_model": attachment.res_model,
                            "res_id": attachment.res_id,
                            "type": attachment.type,
                            "url": attachment.url,
                        }
                    )
