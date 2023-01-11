# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class Base(models.AbstractModel):

    _inherit = 'base'

    def get_selection_label(self, field_name):
        field = self._fields.get(field_name)
        selection = field._description_selection(self.env)
        value = self[field_name]
        return next((label for key, label in selection if key == value), None)
