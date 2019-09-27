# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import api, models


def _get_arch_without_private_fields(env: api.Environment, model: str, arch: str):
    private_fields = env['ir.private.field'].get_model_private_fields(model)
    if not private_fields:
        return arch

    tree = etree.fromstring(arch)

    all_field_nodes = tree.xpath("//field")
    private_field_nodes = (n for n in all_field_nodes if n.attrib.get('name') in private_fields)

    for node in private_field_nodes:
        parent_node = node.getparent()
        parent_node.remove(node)

    return etree.tostring(tree)


class ViewWithPrivateFieldsRemoved(models.Model):
    """Remove private fields from views if user is unauthorized."""

    _inherit = 'ir.ui.view'

    @api.model
    def postprocess_and_fields(self, model, node, view_id):
        """Add custom labels to the view xml.

        This method is called in Odoo when generating the final xml of a view.
        """
        arch, fields = super().postprocess_and_fields(model, node, view_id)

        if not self.env.user.has_private_data_access():
            arch = _get_arch_without_private_fields(self.env, model, arch)

        return arch, fields
