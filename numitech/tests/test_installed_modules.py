
from odoo.tests import TransactionCase


class TestModules(TransactionCase):
    """
    Numitech mainly installs modules for our quality.
    This test suite enforces that the wanted modules are installed.
    """

    def setUp(self):
        super(TestModules, self).setUp()
        self.modules = self.env['ir.module.module']

    def test_sentry(self):
        """ Sentry is installed."""
        self.assertTrue(self.modules.search([('name', '=', 'sentry')]))

    def test_auto_back(self):
        """ Auto Backup is installed."""
        self.assertTrue(self.modules.search([('name', '=', 'auto_backup')]))
