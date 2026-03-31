# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class IrUiView(models.Model):
    _inherit = "ir.ui.view"

    def _remove_write_access_buttons(self, model_name, node):
        """
        Remove object-type buttons from the node if they are not explicitly allowed.
        Allowed buttons are fetched via 'get_read_access_actions()'.

        :param str model_name: The name of the model.
        :param Element node: The lxml node representing the view (or subview).
        """
        read_access_buttons = self.env[model_name].get_read_access_actions()
        for button in node.xpath(".//button[@type='object']"):
            is_read_access_button = button.attrib.get("name") in read_access_buttons
            if not is_read_access_button:
                button.getparent().remove(button)

    def _postprocess_access_rights(self, tree):
        """
        Override to apply extended security rules based on the user's authorization.

        This method is perfectly suited for user-dependent rules because it is
        executed dynamically per request. It operates on the cached view
        architecture, preventing cross-user caching bugs.

        :param Element tree: The lxml etree of the view.
        :return: The modified lxml etree.
        """
        rule_model = self.env["extended.security.rule"]

        # In Odoo 18, both the main view and nested subviews (e.g., inside one2many fields)
        # have the 'model_access_rights' attribute set prior to this method's super call.
        for node in tree.xpath('//*[@model_access_rights]'):
            model_name = node.get('model_access_rights')

            perm_write = rule_model.is_user_authorized(model_name, "write")
            perm_create = rule_model.is_user_authorized(model_name, "create")
            perm_unlink = rule_model.is_user_authorized(model_name, "unlink")

            # Handle relational field tags (e.g., Many2one, Many2many)
            if node.tag == 'field':
                if not perm_write:
                    node.set("can_write", "False")
                if not perm_create:
                    node.set("can_create", "False")

            # Handle standard views (list, form, kanban, etc.)
            else:
                if not perm_write:
                    node.set("edit", "false")
                    self._remove_write_access_buttons(model_name, node)
                if not perm_create:
                    node.set("create", "false")
                if not perm_unlink:
                    node.set("delete", "false")

        # Let standard Odoo logic execute (this will also pop 'model_access_rights' attributes)
        return super()._postprocess_access_rights(tree)