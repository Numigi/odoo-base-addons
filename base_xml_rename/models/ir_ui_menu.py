# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from .xml_rename_mixin import is_lang_installed


class IrUiMenu(models.Model):

    _inherit = ('ir.ui.menu', 'xml.rename.mixin')
    _name = 'ir.ui.menu'

    @api.model
    def rename(self, ref, lang, value, field='name'):
        super().rename(ref, lang, value, field)

        menu = self.env.ref(ref)
        should_update_action_name = (
            is_lang_installed(self.env, lang) and
            menu.action and field == 'name'
        )
        if should_update_action_name:
            menu.action.with_context(lang=lang).name = value
