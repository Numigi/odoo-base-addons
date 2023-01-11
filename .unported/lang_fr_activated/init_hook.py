# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID
from odoo.api import Environment


def post_init_hook(cr, _):
    env = Environment(cr, SUPERUSER_ID, {})
    activate_fr_lang_if_inactive(env)


def activate_fr_lang_if_inactive(env):
    lang = env.ref("base.lang_fr")
    if not lang.active:
        env["res.lang"].load_lang("fr_FR")
