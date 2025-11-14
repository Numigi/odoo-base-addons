# © Numigi (tm) and all its contributors (https://numigi.com/r/home)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from . import models

from odoo import api, fields, SUPERUSER_ID, _


def crm_refresh_res_setting(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Recalculate computed fields of res.config.setting
    env["res.config.settings"].search([]).write({})
