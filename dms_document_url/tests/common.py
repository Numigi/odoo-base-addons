# © 2022 - Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import uuid

from odoo.addons.dms.tests import DocumentsBaseCase


class DocumentsURLBaseCase(DocumentsBaseCase):

    def create_file_with_context(
        self, context, directory=False, content=False, storage=False, sudo=False
    ):
        model = self.file.sudo() if sudo else self.file
        if not directory:
            directory = self.create_directory(storage=storage, sudo=sudo)
        return model.with_context(context).create(
            {
                "name": uuid.uuid4().hex,
                "directory_id": directory.id,
                "content": content or self.content_base64(),
                "type": "binary",
                "url": False,
            }
        )

    def create_attachment(
        self, name, res_model=False, res_id=False, content=False, sudo=False
    ):
        model = self.attachment.sudo() if sudo else self.attachment
        return model.create(
            {
                "name": name,
                "res_model": res_model,
                "res_id": res_id,
                "datas": content or self.content_base64(),
                "type": "binary",
                "url": False,
            }
        )
