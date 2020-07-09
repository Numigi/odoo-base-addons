# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _


class MailTemplate(models.Model):
    _inherit = 'mail.template'
    
    default_template = fields.Boolean("Default Template")
    
    _sql_constraints = [
        ('default_template_uniq', 
         'unique(model_id, default_template)', 
         'This object has already a default template associated.\n You cannot assign more than one default template by object.'),
    ]