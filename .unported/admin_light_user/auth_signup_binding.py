# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ResPartner(models.Model):
    """Add missing access to fields on res.partner when creating a user.

    See TA#6395 and module auth_signup from the odoo code base.
    """

    _inherit = 'res.partner'

    signup_token = fields.Char(
        groups="admin_light_user.group_user_management,base.group_erp_manager")
    signup_type = fields.Char(
        groups="admin_light_user.group_user_management,base.group_erp_manager")
    signup_expiration = fields.Datetime(
        groups="admin_light_user.group_user_management,base.group_erp_manager")
