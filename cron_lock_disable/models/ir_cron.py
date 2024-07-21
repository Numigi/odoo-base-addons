# Copyright 2024 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import os
import logging
from odoo import models

_logger = logging.getLogger(__name__)

ODOO_CRON_LOCK_DISABLE = "ODOO_CRON_LOCK_DISABLE"


class IrCron(models.Model):

    _inherit = "ir.cron"

    def _try_lock(self):
        if self._should_block_lock():
            self._lock_blocked()
        else:
            super()._try_lock()

    def _should_block_lock(self):
        return os.environ.get(ODOO_CRON_LOCK_DISABLE)

    def _lock_blocked(self):
        _logger.info("Locking on the table ir_cron blocked")
