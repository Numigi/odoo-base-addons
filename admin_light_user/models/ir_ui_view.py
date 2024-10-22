# © 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class View(models.Model):
    _inherit = "ir.ui.view"

    def get_inheriting_views_arch(self, model):
        """
        Override the method to filter out the inheritance of
        'admin_light_user'  module views when the user belongs
        to both the 'Admin' and 'Admin Light User' groups.

        This fix is related to ticket TA#68617, where inheriting views from
        the 'admin_light_user' module caused issues for users who are both
        administrators and admin light users. To prevent this,
        the view 'admin_light_user.user_groups_view_without_admin_applications'
        is excluded for such users.

        """

        res = super(View, self).get_inheriting_views_arch(model)
        user = self.env.user

        if (
            self == self.env.ref("base.view_users_form")
            and user.has_group("admin_light_user.group_user_management")
            and user.has_group("base.group_erp_manager")
        ):
            own_view_id = self.env.ref(
                "admin_light_user.user_groups_view_without_admin_applications"
            ).id
            res = res.filtered(lambda v: v.id != own_view_id)

        return res
