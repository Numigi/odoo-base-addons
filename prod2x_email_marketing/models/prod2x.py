# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
import logging

_logger = logging.getLogger(__name__)


class Prod2x(models.AbstractModel):

    _inherit = "prod2x"

    def run(self):
        super().run()
        _logger.info("Anonymizing email marketing contacts")
        self._cr.execute(
            "UPDATE mailing_contact SET email = CONCAT(id, '@example.com')")
