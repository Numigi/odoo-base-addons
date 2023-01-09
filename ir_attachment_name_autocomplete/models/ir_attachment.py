# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class IrAttachmentNameAutoComplete(models.Model):
    """ Set the name of the attachment if the name is not set."""
    _inherit = 'ir.attachment'

    @api.onchange('datas')
    def _compute_name(self):
        """ As soon as a file is uploaded by the user, the name is updated
        using the name if the file.

        Known weakness:
            * hard to test as the behaviour between the api and the GUI is different.
                The name is required as soon as we want to create the attachment from the API.
            * if the user re-upload, the name won't be updated again, and the name of
                old file will stays.
        """
        nameless_attachments = (
            attachment for attachment in self
            if not attachment.name
        )
        for attachment in nameless_attachments:
            attachment.name = attachment.datas_fname
