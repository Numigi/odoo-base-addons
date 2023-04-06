# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import api, models

_logger = logging.getLogger(__name__)


class Prod2x(models.AbstractModel):

    _inherit = "prod2x"

    @api.model
    def run(self):
        super().run()
        self._deactivate_cdn()

    def _deactivate_cdn(self):
        _logger.info("Running CDN deactivation")

        websites = self.env["website"].search([])
        for website in websites:
            website.cdn_activated = False
            _logger.info(
                "CDN deactivated for website {}".format(website.domain))
