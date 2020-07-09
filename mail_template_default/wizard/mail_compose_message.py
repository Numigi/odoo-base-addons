# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'
    
    @api.model
    def default_get(self, fields):
        """ Handle composition mode. Some details about context keys:
            - comment: default mode, model and ID of a record the user comments
                - default_model or active_model
                - default_res_id or active_id
                - default_template
        """
        result = super(MailComposer, self).default_get(fields)
        
        # default values according to default mail template
        default_template_id = self.get_default_template_id(result['model'])
        result['template_id'] = default_template_id
        return result
    
    def get_default_template_id(self, model_id):
        """ Get the mail template that is a default template for the object model_id """
        mail_template_obj = self.env['mail.template']
        
        mail_template_ids = mail_template_obj.search([('model_id','=',model_id),
                                                      ('default_template','=',True)])
        if mail_template_ids:
            return mail_template_ids[0].id
        else:
            return False
        