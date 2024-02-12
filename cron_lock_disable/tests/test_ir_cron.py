# © 2021 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import os
from unittest.mock import patch
from odoo.tests import SavepointCase
from ..models.ir_cron import ODOO_CRON_LOCK_DISABLE


class TestIrCron(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cron = cls.env.ref("base.autovacuum_job")

    @patch.dict(os.environ, {ODOO_CRON_LOCK_DISABLE: "true"})
    def test_lock_blocked(self):
        with self._mock_lock_blocked() as mock_method:
            self.cron.write({"name": "New Name"})
            mock_method.assert_called()

    def test_lock_not_blocked(self):
        with self._mock_lock_blocked() as mock_method:
            self.cron.write({"name": "New Name"})
            mock_method.assert_not_called()

    def _mock_lock_blocked(self):
        cron_class = self.env["ir.cron"].__class__
        return patch.object(cron_class, '_lock_blocked')
