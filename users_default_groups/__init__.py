# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from . import models
from odoo import api, SUPERUSER_ID


def _defaut_config_param(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.config_parameter"].set_param("base_setup.default_user_rights", "1")
