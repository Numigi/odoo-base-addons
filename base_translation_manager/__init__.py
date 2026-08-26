# Copyright 2026 Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from . import models
from . import wizard


def _get_installed_modules(env):
    # Fetch all modules that are currently installed in the database
    return env["ir.module.module"].search([("state", "=", "installed")])


def post_init_hook(env):
    # Force translation reload immediately after the module installation is complete
    installed_modules = _get_installed_modules(env)
    installed_modules._update_translations(["fr_FR"], True)
