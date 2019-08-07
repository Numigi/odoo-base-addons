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

    def check_extended_security_all(self):
        """Check extended security rules that applies for all CRUD operations."""
        pass

    def check_extended_security_read(self):
        """Check extended security rules for read operations."""
        pass

    def check_extended_security_write(self):
        """Check extended security rules for write operations."""
        pass

    def check_extended_security_create(self):
        """Check extended security rules for create operations."""
        pass

    def check_extended_security_unlink(self):
        """Check extended security rules for unlink operations."""
        pass
