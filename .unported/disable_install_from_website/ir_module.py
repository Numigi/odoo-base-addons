# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import models, api, _
from odoo.addons.base.models.ir_module import assert_log_admin_access
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Module(models.Model):

    _inherit = 'ir.module.module'

    @assert_log_admin_access
    @api.multi
    def button_immediate_install(self):
        """ Disable install of selected modules.
        """
        raise UserError(_("Install of modules through the interface is disable. "
                          "Contact your Odoo Partner for more details."))
