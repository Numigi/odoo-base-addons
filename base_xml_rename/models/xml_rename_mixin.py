# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import api, models
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


def is_lang_installed(env: 'Environment', lang: str):
    return lang in dict(env['res.lang'].get_installed())


class XMLRenameMixin(models.AbstractModel):

    _name = 'xml.rename.mixin'
    _description = 'Mixin For Renaming Records Through XML'

    @api.model
    def rename(self, ref, lang, value, field='name'):
        """Rename the record to rename.

        :param ref: the XML ID of the record to rename
        :param lang: the language of the term
        :param value: the new name for the record
        """
        if not is_lang_installed(self.env, lang):
            _logger.debug(
                'Skip renaming the record {ref} for the language {lang}. '
                'The language is not installed.'
                .format(ref=ref, lang=lang)
            )
            return

        _logger.info(
            'Renaming the record {ref} with the label `{value}` '
            'for the language {lang}.'
            .format(ref=ref, lang=lang, value=value)
        )
        record = self.env.ref(ref)
        if record._name != self._name:
            raise ValidationError(
                'The XML ID {ref} does not reference a record of model {model}. '
                'It references a record of model {record_model}'
                .format(ref=ref, model=self._name, record_model=record._name)
            )

        record.with_context(lang=lang).write({field: value})
