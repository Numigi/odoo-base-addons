# Copyright 2024 Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class TranslateTermFrCA(models.Model):

    _name = "translate.term.fr_ca"
    _description = "Translation Term Mapping"

    term_fr = fields.Char("Term (French)", required=True)
    term_ca = fields.Char("Term (Canadian French)", required=True)
    modules = fields.Many2many(
        "ir.module.module",
        "rel_modules_fr_ca_labels",
        string="Modules",
        domain=[("state", "=", "installed")],
    )
