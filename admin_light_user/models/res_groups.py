# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


ADMIN_LIGHT_USER_VIEW = "admin_light_user.user_groups_view_without_admin_applications"


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
