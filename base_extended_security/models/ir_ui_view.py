# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models
from odoo.tests.common import  Form

import xml.etree.ElementTree as ET


class ViewWithButtonsHiden(models.Model):

    _inherit = "ir.ui.view"

    @api.model
    def postprocess_and_fields(self, node, model=None, **options):
        """Add custom labels to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, models = super().postprocess_and_fields(node, model, **options)

        is_nested_view = bool(self.env.context.get("base_model_name"))
        if not is_nested_view and model:
           # arch = _hide_buttons_with_access_blocked(self.env, model, arch)
            one2may_fields = get_one2many_fields(self.env,models)
            view_arch= etree.fromstring(arch)

            for field in one2may_fields :

                field_node = view_arch.xpath("//field[@name='%s']"%field.name)[0]
                #
                if field_node:
                    node = etree.tostring(field_node, encoding="unicode").replace('\t', '')
                    print("111111111",field.name,field.model_id.model,type(node),node)
                    tree_node =  ET.fromstring(node).find('tree')
                    if tree_node is not None:
                        tree_content = ET.tostring(tree_node, encoding='unicode',
                        method='xml')
                        print("222222-treee_conten",tree_content)
                        _hide_buttons_with_access_blocked(self.env,field.model_id.model, tree_content)
                    else:
                        print("No <tree> element found")




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
        print("3333333333333333333")
        return arch

    tree = etree.fromstring(arch)
    print("3333333333333",tree,arch)
    if not perm_write:
        tree.attrib["edit"] = "false"
        _remove_write_access_buttons(env, model, tree)
        print("perm_write")
    if not perm_create:
        print("perm_create")
        tree.attrib["create"] = "false"

    if not perm_unlink:
        print("perm_unlink")
        tree.attrib["delete"] = "false"

    return etree.tostring(tree)


def _remove_write_access_buttons(env, model, tree):
    read_access_buttons = env[model].get_read_access_actions()
    for button in tree.xpath("//button[@type='object']"):
        is_read_access_button = button.attrib.get("name") in read_access_buttons
        if not is_read_access_button:
            button.getparent().remove(button)


def _hide_one2many_view_buttons_with_access_blocked(env, models):
    """Hide the buttons in nested one2many fields with access restricted.

    The view architectures are updated directly inside the field
    definition if required.

    :param env: the Odoo environment
    :param fields: the field definitions
    """
    one2many_fields = get_one2many_fields(env,models)
    for rec in one2many_fields:
        model = rec.model_id.id

        #one2many_fields['arch'] = _hide_buttons_with_access_blocked(env, model, one2many_fields['arch'])

def get_one2many_fields(env,models):
    res=[]
    for key in models:
        for field in models[key]:
            field_id = env['ir.model.fields'].search([('name','=',field),
                                                      ('model','=',key)])
            if field_id.ttype == 'one2many':
                res.append(field_id)
    return res
