# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models


class ViewWithButtonsHiden(models.Model):
    _inherit = "ir.ui.view"

    def _remove_write_access_buttons(self, env, model, tree):
        read_access_buttons = env[model].get_read_access_actions()
        for button in tree.xpath("//button[@type='object']"):
            is_read_access_button = button.attrib.get("name") in read_access_buttons
            if not is_read_access_button:
                button.getparent().remove(button)

    def _hide_buttons_with_access_blocked(self, env, model, arch):
        perm_write = env["extended.security.rule"].is_user_authorized(model, "write")
        perm_create = env["extended.security.rule"].is_user_authorized(model, "create")
        perm_unlink = env["extended.security.rule"].is_user_authorized(model, "unlink")

        has_full_access = perm_write and perm_create and perm_unlink

        if has_full_access:
            return arch
        tree = etree.fromstring(arch)

        if not perm_write:
            tree.attrib["edit"] = "false"
            self._remove_write_access_buttons(env, model, tree)

        if not perm_create:
            tree.attrib["create"] = "false"

        if not perm_unlink:
            tree.attrib["delete"] = "false"

        return etree.tostring(tree)

    def get_one2many_fields(self, env, models):
        res = []
        for key in models:
            for field in models[key]:
                field_id = env["ir.model.fields"].search(
                    [("name", "=", field), ("model", "=", key)]
                )
                if field_id.ttype == "one2many":
                    res.append(field_id)
        return res

    def _hide_one2many_view_buttons_with_access_blocked(self, models, arch):
        """Hide the buttons in nested one2many fields with access restricted.

        The view architectures are updated directly inside the field
        definition if required.

        :param env: the Odoo environment
        :param fields: the field definitions"""
        one2many_fields = self.get_one2many_fields(self.env, models)
        view_arch = etree.fromstring(arch)

        for field in one2many_fields:
            xpath = f"//field[@name='{field.name}']"
            for field_node in view_arch.xpath(xpath):
                tree_node = field_node.find("tree")
                if tree_node is not None:
                    tree_content = etree.tostring(tree_node, encoding="unicode")
                    modified_content = self._hide_buttons_with_access_blocked(
                        self.env, field.relation, tree_content
                    )
                    field_node.remove(tree_node)
                    field_node.append(etree.fromstring(modified_content))
        return view_arch

    @api.model
    def postprocess_and_fields(self, node, model=None, **options):
        arch, models = super().postprocess_and_fields(node, model, **options)
        is_nested_view = bool(self.env.context.get("base_model_name"))

        if not is_nested_view and model:
            arch = self._hide_buttons_with_access_blocked(self.env, model, arch)
            view_arch = self._hide_one2many_view_buttons_with_access_blocked(
                models, arch
            )
            arch = etree.tostring(view_arch, encoding="unicode")
        return arch, models
