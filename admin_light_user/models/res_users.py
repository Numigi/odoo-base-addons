# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import models, api, _
from odoo.exceptions import AccessError


SUPER_ADMIN_APPLICATIONS = [
    "admin_light_base.module_category_admin",
    "base.module_category_administration_administration",
    "base.module_category_hidden",
    "base.module_category_usability",
]
ADMIN_LIGHT_USER_VIEW = "admin_light_user.user_groups_view_without_admin_applications"

ADMIN_GROUPS = [
    "base.group_erp_manager",
    "base.group_system",
    "admin_light_base.group_admin",
]


def _remove_admin_application_checkbox_fields(
    tree: etree._Element, env: api.Environment
):
    """Remove checkbox fields of groups related to super admin applications from the view tree.

    :param tree: the xml tree of the view to modify.
    :param env: the odoo environment
    """
    admin_applications = [env.ref(app) for app in SUPER_ADMIN_APPLICATIONS]

    checkbox_group_fields = tree.xpath("//field[starts-with(@name, 'in_group_')]")
    for node in checkbox_group_fields:
        selected_group_id = int(node.attrib["name"].replace("in_group_", ""))
        selected_group = env["res.groups"].browse(selected_group_id)
        if selected_group.category_id in admin_applications:
            node.getparent().remove(node)


def _remove_separators_with_no_fields_below(tree: etree._Element):
    """Remove separators with no fields below from the view tree.

    :param tree: the xml tree of the view to modify.
    """
    seperators = tree.xpath("//separator")
    group_administration = tree.xpath("//group[@string='Administration']")
    for node in seperators + group_administration:
        sibling_node = node.getnext()
        if sibling_node is None or sibling_node.tag != "field":
            node.getparent().remove(node)


def _remove_admin_application_selection_fields(
    tree: etree._Element, env: api.Environment
):
    """Remove selection fields of groups related to super admin applications from the view tree.

    :param tree: the xml tree of the view to modify.
    :param env: the odoo environment
    """
    admin_applications = [env.ref(app) for app in SUPER_ADMIN_APPLICATIONS]

    selection_group_fields = tree.xpath("//field[starts-with(@name, 'sel_groups')]")
    for node in selection_group_fields:
        selected_group_ids = [
            int(g) for g in node.attrib["name"].replace("sel_groups_", "").split("_")
        ]
        selected_groups = env["res.groups"].browse(selected_group_ids)
        if selected_groups[0].category_id in admin_applications:
            node.getparent().remove(node)


class ResUsers(models.Model):

    _inherit = "res.users"

    @api.model
    def create(self, vals):
        if self.env.user.has_group("admin_light_user.group_user_management"):
            self._check_not_granting_admin_priviledges(vals)

        return super().create(vals)

    def write(self, vals):
        if self.env.user.has_group("admin_light_user.group_user_management"):
            self._check_not_granting_admin_priviledges(vals)
            self._check_not_unarchiving_admin(vals)

        return super().write(vals)

    def _check_not_granting_admin_priviledges(self, vals):
        groups_id = vals.get("groups_id", [])

        admin_group_ids = {self.env.ref(group_ref).id for group_ref in ADMIN_GROUPS}

        is_granting_admin = any(
            (command[0] == 4 and command[1] in admin_group_ids)
            or (command[0] == 6 and set(command[2]) & admin_group_ids)
            for command in groups_id
        )

        if is_granting_admin:
            raise AccessError(
                _(
                    "You are not authorized to grant admin priviledges. "
                    "Only the super admin can."
                )
            )

    def _check_not_unarchiving_admin(self, vals):
        if "active" in vals:
            super_admin_group = self.env.ref("base.group_erp_manager")
            if super_admin_group in self.mapped("groups_id"):
                raise AccessError(
                    _(
                        "You are not authorized to archive or unarchive a user with "
                        "super admin priviledges. "
                        "Only the super admin can."
                    )
                )

    @api.model
    def update_admin_light_user_group_view(self):
        """Update the content of the admin light user form.

        This form is the same as the standard admin form view but with the groups
        related to super admin applications removed.
        """
        admin_view = self.env.ref("base.user_groups_view")
        admin_view_tree = etree.fromstring(admin_view.arch)

        _remove_admin_application_selection_fields(admin_view_tree, self.env)
        _remove_admin_application_checkbox_fields(admin_view_tree, self.env)
        _remove_separators_with_no_fields_below(admin_view_tree)

        xml_content = etree.tostring(
            admin_view_tree, pretty_print=True, encoding="unicode"
        )
        admin_light_view = self.env.ref(ADMIN_LIGHT_USER_VIEW)
        admin_light_view.write({"arch": xml_content})

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(
            view_id=view_id,
            view_type=view_type,
            toolbar=toolbar,
            submenu=submenu
        )
        view_user_form_id = self.env.ref("base.view_users_form").id
        if view_type == "form" and view_id == view_user_form_id:
            user = self.env.user
            if user.has_group("base.group_erp_manager") :
                return res
            elif user.has_group("admin_light_user.group_user_management") :
                arch = etree.XML(res["arch"])
                _remove_admin_application_selection_fields(arch, self.env)
                _remove_admin_application_checkbox_fields(arch, self.env)
                _remove_separators_with_no_fields_below(arch)
                res.update({
                    "arch" : etree.tostring(arch, pretty_print=True, encoding="unicode")
                })
        return res
