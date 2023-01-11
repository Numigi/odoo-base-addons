# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class IrActionsViewModeRestriction(models.Model):

    _name = 'ir.actions.view.mode.restriction'
    _description = 'Ir Action View Mode Restriction'

    action_id = fields.Many2one(
        'ir.actions.act_window',
        required=True,
        index=True,
    )

    view_modes = fields.Char(required=True)

    group_ids = fields.Many2many(
        "res.groups",
        "ir_actions_view_mode_restriction_group_rel",
        "restriction_id",
        "group_id",
        required=True,
    )

    def _get_view_mode_list(self):
        return [
            mode.strip() for mode in self.view_modes.split(",")
        ]
