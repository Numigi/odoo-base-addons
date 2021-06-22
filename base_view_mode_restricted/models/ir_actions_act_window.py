# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from itertools import chain
from odoo import api, fields, models


class IrActionsActWindow(models.Model):

    _inherit = "ir.actions.act_window"

    view_mode_restriction_ids = fields.One2many(
        "ir.actions.view.mode.restriction",
        "action_id",
    )

    def _compute_views(self):
        super()._compute_views()
        for action in self:
            action.views = action._get_authorized_views()

    def _get_authorized_views(self):
        forbiden_modes = self._get_forbiden_view_modes()
        return [
            (view_id, mode)
            for view_id, mode in self.views
            if mode not in forbiden_modes
        ]

    def _get_forbiden_view_modes(self):
        user_groups = self.env.user.groups_id
        restrictions = self.view_mode_restriction_ids.filtered(
            lambda r: not (r.group_ids & user_groups)
        )
        return set(chain.from_iterable(r._get_view_mode_list() for r in restrictions))
