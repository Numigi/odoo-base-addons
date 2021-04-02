# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models
from typing import Iterable


class ViewWithButtonsHiden(models.Model):

    _inherit = 'ir.ui.view'

    def postprocess_and_fields(self, node, model=None, validate=False):
        """Add custom labels to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, fields = super().postprocess_and_fields(node, model=model, validate=validate)

        is_nested_view = bool(self._context.get('base_model_name'))
        view_model = model or self.model

        if not is_nested_view and view_model:
            arch = _hide_buttons_with_access_blocked(self.env, view_model, arch)
            _hide_one2many_view_buttons_with_access_blocked(self.env, fields)

        return arch, fields


def _hide_buttons_with_access_blocked(env, model, arch):
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
        _remove_object_button_tags(tree)

    if not perm_create:
        tree.attrib['create'] = "false"

    if not perm_unlink:
        tree.attrib['delete'] = "false"

    return etree.tostring(tree)


def _remove_object_button_tags(tree):
    for button in tree.xpath("//button[@type='object']"):
        button.getparent().remove(button)


def _hide_one2many_view_buttons_with_access_blocked(env, fields):
    """Hide the buttons in nested one2many fields with access restricted.

    The view architectures are updated directly inside the field
    definition if required.

    :param env: the Odoo environment
    :param fields: the field definitions
    """
    one2many_fields = (f for f in fields.values() if f['type'] == 'one2many')
    for field in one2many_fields:
        model = field['relation']

        for view in field['views'].values():
            view['arch'] = _hide_buttons_with_access_blocked(env, model, view['arch'])
