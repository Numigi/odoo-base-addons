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
        return self.env['extended.security.rule'].get_user_security_domain(
            model=self._name
        )

    def check_extended_security_all(self):
        """Check extended security rules that applies for all CRUD operations.

        This method excludes the name_get operation.

        The reason is that name_get is much less likely to be a security
        issue for most use cases.

        Blocking name_get also causes errors in the web.interface,
        because of Many2one fields.
        """
        pass

    def check_extended_security_read(self):
        """Check extended security rules for read operations."""
        self.env['extended.security.rule'].check_user_access(
            model=self._name, access_type='read',
        )

    def check_extended_security_write(self):
        """Check extended security rules for write operations."""
        self.env['extended.security.rule'].check_user_access(
            model=self._name, access_type='write',
        )

    def check_extended_security_create(self):
        """Check extended security rules for create operations."""
        self.env['extended.security.rule'].check_user_access(
            model=self._name, access_type='create',
        )

    def check_extended_security_unlink(self):
        """Check extended security rules for unlink operations."""
        self.env['extended.security.rule'].check_user_access(
            model=self._name, access_type='unlink',
        )
