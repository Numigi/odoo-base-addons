# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models


class ViewWithButtonsHiden(models.Model):

    _inherit = "ir.ui.view"

    @api.model
    def postprocess_and_fields(self, node, model=None, **options):
        """Add custom labels to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, models = super().postprocess_and_fields(node, model, **options)
        is_nested_view = bool(self._context.get("base_model_name"))
        if not is_nested_view and model:
            arch = _hide_buttons_with_access_blocked(self.env, model, arch)
            _hide_one2many_view_buttons_with_access_blocked(self.env, models, arch)

        return arch, models


def _hide_buttons_with_access_blocked(env, model, arch):
    """Hide buttons on the view for which the user access is blocked.

    :param env: the Odoo environment
    :param model: the model of the view
    :param arch: the view xml before applying rules
    :return: the view xml with proper button access.
    """
    perm_write = env["extended.security.rule"].is_user_authorized(model, "write")
    perm_create = env["extended.security.rule"].is_user_authorized(model, "create")
    perm_unlink = env["extended.security.rule"].is_user_authorized(model, "unlink")

    has_full_access = perm_write and perm_create and perm_unlink
    if has_full_access:
        return arch

    tree = etree.fromstring(arch)

    if not perm_write:
        tree.attrib["edit"] = "false"
        _remove_write_access_buttons(env, model, tree)

    if not perm_create:
        tree.attrib["create"] = "false"

    if not perm_unlink:
        tree.attrib["delete"] = "false"

    return etree.tostring(tree)


def _remove_write_access_buttons(env, model, tree):
    read_access_buttons = env[model].get_read_access_actions()
    for button in tree.xpath("//button[@type='object']"):
        is_read_access_button = button.attrib.get("name") in read_access_buttons
        if not is_read_access_button:
            button.getparent().remove(button)


def _hide_one2many_view_buttons_with_access_blocked(env, models, arch):
    """Hide the buttons in nested one2many fields with access restricted.

    The view architectures are updated directly inside the field
    definition if required.

    :param env: the Odoo environment
    :param fields: the field definitions
    """
    one2many_fields = get_one2many_fields(env,models,arch)
    for rec in one2many_fields.items():
        model = one2many_fields['field'].model_id.id
        res = _hide_buttons_with_access_blocked(env, model, one2many_fields['arch'])

def get_one2many_fields(env,models,arch):
    res={}
    for key in models:
        for field in models[key]:
            field_id = env['ir.model.fields'].search([('name','=',field),
                                                      ('model','=',key)])
            if field_id.ttype == 'one2many':
                res['field']= field_id
                res['arch']= arch
    return res
