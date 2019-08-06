# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class BaseWithExtendedSecurity(models.AbstractModel):

    _inherit = 'base'

    def get_extended_security_domain(self):
        """Get a search domain to apply to securize requests.

        This method returns an empty domain.

        Specific modules can inherit models to restrict the search domain.
        See the unit tests of this module for concrete examples.

        :rtype: list
        """
        return []
