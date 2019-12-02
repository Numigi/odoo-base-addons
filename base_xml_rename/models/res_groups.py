# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import api, models
from odoo.exceptions import ValidationError
from .common import is_lang_installed, rename_record


_logger = logging.getLogger(__name__)


class ResGroups(models.Model):

    _inherit = 'res.groups'

    @api.model
    def rename(self, group_ref, lang, value):
        """Rename the user group.

        :param group_ref: the XML ID of the group
        :param lang: the language of the group
        :param value: the new name for the group
        """
        if not is_lang_installed(self.env, lang):
            _logger.debug(
                'Skip renaming user group {group_ref} for the language {lang}. '
                'The language is not installed.'
                .format(group_ref=group_ref, lang=lang)
            )
            return

        _logger.info(
            'Renaming the user group {group_ref} with the label `{value}` '
            'for the language {lang}.'
            .format(group_ref=group_ref, lang=lang, value=value)
        )
        group = self.env.ref(group_ref)
        if group._name != self._name:
            raise ValidationError(
                'The XML ID {} does not reference a group.'
                .format(group_ref)
            )

        rename_record(group, lang, value)
