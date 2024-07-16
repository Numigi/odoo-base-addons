# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class IrAttachmentTokenAccessPortal(models.Model):
    """
    Allow portal user to access the ir.attachments of tasks.
    see ref: TA#6109
    """

    _inherit = "ir.attachment"

    access_token = fields.Char(groups="base.group_user,base.group_portal")

    def generate_access_token(self):
        """
        Grant sudo access to the field ir_attachment.access_token

        It prevents to give write rights to ir.attachments and project.task to group_portal.
        see ref: TA#6109
        """
        return super(IrAttachmentTokenAccessPortal, self.sudo()).generate_access_token()
