# Copyright 2025-today Numigi and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
