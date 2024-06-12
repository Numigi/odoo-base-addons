# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
import logging

_logger = logging.getLogger(__name__)


class Prod2x(models.AbstractModel):

    _inherit = "prod2x"

    def run(self):
        super().run()
        _logger.info("Deactivating domain")
        websites = self.env["website"].search([])
        for website in websites:
            self._disable_website_domain(website)

    def _disable_website_domain(self, website):
        _logger.info(f"Deactivating {website.domain} from {website.name}")
        website.domain = ""
