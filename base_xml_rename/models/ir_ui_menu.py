# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import api, models
from odoo.exceptions import ValidationError
from .common import is_lang_installed, rename_record


_logger = logging.getLogger(__name__)


class IrUiMenu(models.Model):

    _inherit = 'ir.ui.menu'

    @api.model
    def rename(self, menu_ref, lang, value):
        """Rename the menu item.

        :param menu_ref: the XML ID of the menu item
        :param lang: the language of the menu entry
        :param value: the new name for the menu entry
        """
        if not is_lang_installed(self.env, lang):
            _logger.debug(
                'Skip renaming menu item {menu_ref} for the language {lang}. '
                'The language is not installed.'
                .format(menu_ref=menu_ref, lang=lang)
            )
            return

        _logger.info(
            'Renaming menu item {menu_ref} with the label `{value}` '
            'for the language {lang}.'
            .format(menu_ref=menu_ref, lang=lang, value=value)
        )
        menu = self.env.ref(menu_ref)
        if menu._name != self._name:
            raise ValidationError(
                'The XML ID {} does not reference a menu item.'
                .format(menu_ref)
            )

        rename_record(menu, lang, value)

        if menu.action:
            rename_record(menu.action, lang, value)
