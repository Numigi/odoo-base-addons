# Copyright 2014 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models

SUPER_ADMIN_APPLICATIONS = [
    "admin_light_base.module_category_admin",
    "base.module_category_administration_administration",
    "base.module_category_hidden",
    "base.module_category_usability",
]

ADMIN_LIGHT_USER_VIEW = "base.view_users_form"


class GroupsWithUpdateAdminLightView(models.Model):

    _inherit = "res.groups"

    @api.model
    def _update_user_groups_view(self):
        """After updating the main user/groups view, update the admin light view.

        This method can be loaded before the view is installed. In such case, we skip.
        """
        super()._update_user_groups_view()
        if self.env.ref(ADMIN_LIGHT_USER_VIEW, raise_if_not_found=False):
            self.env["res.users"].update_admin_light_user_group_view()
