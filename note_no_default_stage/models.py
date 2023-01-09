# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import models


_logger = logging.getLogger(__name__)


class User(models.Model):

    _inherit = 'res.users'

    def _create_note_stages(self):
        for user in self:
            _logger.info(
                'No default note columns created for user id {}.'.format(user.id)
            )
