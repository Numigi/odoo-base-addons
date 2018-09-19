# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models

SUPER_ADMIN_APPLICATIONS = [
    'admin_light_base.module_category_admin',
    'base.module_category_administration',
    'base.module_category_hidden',
    'base.module_category_usability',
]

ADMIN_LIGHT_USER_VIEW = 'admin_light_user.user_groups_view_without_admin_applications'


class GroupsWithUpdateAdminLightView(models.Model):

    _inherit = 'res.groups'

    @api.model
    def _update_user_groups_view(self):
        """After updating the main user/groups view, update the admin light view.

        This method can be loaded before the view is installed. In such case, we skip.
        """
        super()._update_user_groups_view()
        if self.env.ref(ADMIN_LIGHT_USER_VIEW, raise_if_not_found=False):
            self.env['res.users'].update_admin_light_user_group_view()


class UsersWithAdminGroupsMasked(models.Model):

    _inherit = 'res.users'

    @api.model
    def update_admin_light_user_group_view(self):
        """Update the content of the admin light user form.

        This form is the same as the standard admin form view but with the groups
        related to super admin applications removed.
        """
        admin_view = self.env.ref('base.user_groups_view')
        admin_view_tree = etree.fromstring(admin_view.arch)

        _remove_admin_application_selection_fields(admin_view_tree, self.env)
        _remove_admin_application_checkbox_fields(admin_view_tree, self.env)
        _remove_separators_with_no_fields_below(admin_view_tree)

        xml_content = etree.tostring(admin_view_tree, pretty_print=True, encoding="unicode")
        admin_light_view = self.env.ref(ADMIN_LIGHT_USER_VIEW)
        admin_light_view.write({'arch': xml_content})


def _remove_admin_application_selection_fields(tree: etree._Element, env: api.Environment):
    """Remove selection fields of groups related to super admin applications from the view tree.

    :param tree: the xml tree of the view to modify.
    :param env: the odoo environment
    """
    admin_applications = [env.ref(app) for app in SUPER_ADMIN_APPLICATIONS]

    selection_group_fields = tree.xpath("//field[starts-with(@name, 'sel_groups')]")
    for node in selection_group_fields:
        selected_group_ids = [
            int(g) for g in node.attrib['name'].replace('sel_groups_', '').split('_')
        ]
        selected_groups = env['res.groups'].browse(selected_group_ids)
        if selected_groups[0].category_id in admin_applications:
            node.getparent().remove(node)


def _remove_admin_application_checkbox_fields(tree: etree._Element, env: api.Environment):
    """Remove checkbox fields of groups related to super admin applications from the view tree.

    :param tree: the xml tree of the view to modify.
    :param env: the odoo environment
    """
    admin_applications = [env.ref(app) for app in SUPER_ADMIN_APPLICATIONS]

    checkbox_group_fields = tree.xpath("//field[starts-with(@name, 'in_group_')]")
    for node in checkbox_group_fields:
        selected_group_id = int(node.attrib['name'].replace('in_group_', ''))
        selected_group = env['res.groups'].browse(selected_group_id)
        if selected_group.category_id in admin_applications:
            node.getparent().remove(node)


def _remove_separators_with_no_fields_below(tree: etree._Element):
    """Remove separators with no fields below from the view tree.

    :param tree: the xml tree of the view to modify.
    """
    seperators = tree.xpath("//separator")
    for node in seperators:
        sibling_node = node.getnext()
        if sibling_node is None or sibling_node.tag != 'field':
            node.getparent().remove(node)
