# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, tools, _
from odoo.exceptions import AccessError


class ExtendedSecurityRule(models.Model):

    _name = 'extended.security.rule'
    _description = "Extended Security Rule"
    _order = 'model_id'

    model_id = fields.Many2one('ir.model', required=True, ondelete='cascade')

    group_ids = fields.Many2many(
        'res.groups',
        'extended_security_rule_group_rel',
        'rule_id',
        'group_id',
    )

    perm_read = fields.Boolean('Read')
    perm_write = fields.Boolean('Write')
    perm_create = fields.Boolean('Create')
    perm_unlink = fields.Boolean('Delete')
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        self.clear_caches()
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        self.clear_caches()
        return res

    @api.multi
    def unlink(self):
        res = super().unlink()
        self.clear_caches()
        return res

    @tools.ormcache('model', 'access_type')
    def _find_matching_rules(self, model, access_type):
        return self.sudo().search([
            ('model_id.model', '=', model),
            ('perm_{}'.format(access_type), '=', True),
        ])

    def _is_user_authorized(self, user):
        return self.group_ids & user.groups_id

    @api.model
    def check_user_access(self, model, access_type):
        for rule in self._find_matching_rules(model, access_type):
            if not rule._is_user_authorized(self.env.user):
                raise AccessError(_(
                    'You are not authorized to access records of model {model} '
                    'in {access_type} mode.',
                ).format(model=model, access_type=_(access_type)))

    @api.model
    def is_user_authorized(self, model, access_type):
        matching_rules = self._find_matching_rules(model, access_type)
        return all(rule._is_user_authorized(self.env.user) for rule in matching_rules)

    @api.model
    def get_user_security_domain(self, model):
        authorized = self.is_user_authorized(model, 'read')
        return [] if authorized else [('id', '=', False)]
