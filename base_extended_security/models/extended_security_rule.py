# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from collections import defaultdict
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

    def write(self, vals):
        res = super().write(vals)
        self.clear_caches()
        return res

    def unlink(self):
        res = super().unlink()
        self.clear_caches()
        return res

    @api.model
    def check_user_access(self, model, access_type):
        for rule in self._iter_matching_rules(model, access_type):
            if not _rule_matches_user(rule, self.env.user):
                raise AccessError(_(
                    'You are not authorized to access records of model {model} '
                    'in {access_type} mode.',
                ).format(model=model, access_type=_(access_type)))

    @api.model
    def is_user_authorized(self, model, access_type):
        matching_rules = self._iter_matching_rules(model, access_type)
        return all(_rule_matches_user(rule, self.env.user) for rule in matching_rules)

    @api.model
    def get_user_security_domain(self, model):
        authorized = self.is_user_authorized(model, 'read')
        return [] if authorized else [('id', '=', False)]

    def _iter_matching_rules(self, model, access_type):
        rules = self._get_rules()
        return (r for r in rules[model] if r[access_type])

    @api.model
    @tools.ormcache()
    def _get_rules(self):
        res = defaultdict(list)
        for record in self.sudo().search([]):
            res[record.model_id.model].append(record._make_rule_dict())
        return res

    def _make_rule_dict(self):
        return {
            "group_ids": self.group_ids.ids,
            "read": self.perm_read,
            "write": self.perm_write,
            "create": self.perm_create,
            "unlink": self.perm_unlink,
        }


def _rule_matches_user(rule, user):
    user_group_ids = user.groups_id.ids
    return any(id_ in user_group_ids for id_ in rule["group_ids"])
