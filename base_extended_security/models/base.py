# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api


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
        """Check extended security rules that applies for all CRUD operations."""
        pass

    def check_extended_security_read(self):
        """Check extended security rules for read operations."""
        self.env['extended.security.rule'].check_user_access(
            model=self._name, access_type='read',
        )
        self.check_extended_security_all()

    def check_extended_security_write(self):
        """Check extended security rules for write operations."""
        self.env['extended.security.rule'].check_user_access(
            model=self._name, access_type='write',
        )
        self.check_extended_security_all()

    def check_extended_security_create(self):
        """Check extended security rules for create operations."""
        self.env['extended.security.rule'].check_user_access(
            model=self._name, access_type='create',
        )
        self.check_extended_security_all()

    def check_extended_security_unlink(self):
        """Check extended security rules for unlink operations."""
        self.env['extended.security.rule'].check_user_access(
            model=self._name, access_type='unlink',
        )
        self.check_extended_security_all()

    @api.model
    def get_read_access_actions(self):
        """Get names of actions that should always appear on form views.

        By default, when a user has only read access to a model,
        the action buttons are hidden.

        This method returns a list of method names.

        Buttons bound to these method will not be hidden by the
        extended security module.
        """
        return []
