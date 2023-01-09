from odoo import models, fields


class IrAttachmentTokenAccessPortal(models.Model):
    """ Allow portal user to access the ir.attachments of tasks.

    see TA#6109
    """
    _inherit = 'ir.attachment'

    access_token = fields.Char(groups="base.group_user,base.group_portal")

    def generate_access_token(self):
        """ Grant sudo access to the field ir_attachment.access_token

        It prevents to give write rights to ir.attachments and project.task to group_portal.
        see TA#6109
        """
        return super(IrAttachmentTokenAccessPortal, self.sudo()).generate_access_token()
