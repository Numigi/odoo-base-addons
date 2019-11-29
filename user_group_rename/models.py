# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import api, models
from odoo.exceptions import ValidationError


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
        _logger.info(
            'Renaming the user group {group_ref} with the label `{value}` '
            'for the language {lang}.'
            .format(group_ref=group_ref, lang=lang, value=value)
        )
        group = self.env.ref(group_ref)
        if group._name != 'res.groups':
            raise ValidationError(
                'The XML ID {} does not reference a group.'
                .format(group_ref)
            )

        group.with_context(lang=lang).name = value
