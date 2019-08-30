# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models


def _hide_buttons_with_access_blocked(env: api.Environment, model: str, arch: str) -> str:
    """Hide buttons on the view for which the user access is blocked.

    :param env: the Odoo environment
    :param model: the model of the view
    :param arch: the view xml before applying rules
    :return: the view xml with proper button access.
    """
    perm_write = env['extended.security.rule'].is_user_authorized(model, 'write')
    perm_create = env['extended.security.rule'].is_user_authorized(model, 'create')
    perm_unlink = env['extended.security.rule'].is_user_authorized(model, 'unlink')

    has_full_access = perm_write and perm_create and perm_unlink
    if has_full_access:
        return arch

    tree = etree.fromstring(arch)

    if not perm_write:
        tree.attrib['edit'] = "false"

    if not perm_create:
        tree.attrib['create'] = "false"

    if not perm_unlink:
        tree.attrib['delete'] = "false"

    return etree.tostring(tree)


class ViewWithButtonsHiden(models.Model):

    _inherit = 'ir.ui.view'

    @api.model
    def postprocess_and_fields(self, model, node, view_id):
        """Add custom labels to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, fields = super().postprocess_and_fields(model, node, view_id)
        arch_with_buttons_hidden = _hide_buttons_with_access_blocked(self.env, model, arch)
        return arch_with_buttons_hidden, fields
