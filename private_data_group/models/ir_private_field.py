# Copyright 2022-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from collections import defaultdict
from odoo import api, fields, models
from odoo.tools import ormcache


class PrivateField(models.Model):

    _name = 'ir.private.field'
    _description = 'Private Field'

    model_id = fields.Many2one(
        'ir.model', 'Model', related='field_id.model_id', store=True,
    )
    model_select_id = fields.Many2one(
        'ir.model',
        compute='_compute_model_select_id',
        inverse=lambda self: None,
    )
    field_id = fields.Many2one('ir.model.fields', required=True, ondelete='cascade')
    active = fields.Boolean(default=True)

    def _compute_model_select_id(self):
        for field in self:
            field.model_select_id = field.model_id

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        self.clear_caches()
        return res

    def write(self, vals):
        res = super().write(vals)
        self.clear_caches()
        return res

    def unlink(self):
        res = super().unlink()
        self.clear_caches()
        return res

    @ormcache()
    def _get_all_items(self):
        fields = self.sudo().search([])
        result = defaultdict(list)
        for f in fields:
            result[f.field_id.model].append(f.field_id.name)
        return result

    @api.model
    def get_model_private_fields(self, model):
        return set(self._get_all_items()[model])

    @api.onchange('model_select_id')
    def _onchange_model_empty_field(self):
        if self.model_select_id != self.field_id.model_id:
            self.field_id = False
