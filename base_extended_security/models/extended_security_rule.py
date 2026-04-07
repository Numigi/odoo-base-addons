# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from collections import defaultdict
from odoo import api, fields, models, tools, _
from odoo.exceptions import AccessError


class ExtendedSecurityRule(models.Model):
    _name = "extended.security.rule"
    _description = "Extended Security Rule"
    _order = "model_id"

    model_id = fields.Many2one("ir.model", required=True, ondelete="cascade")

    group_ids = fields.Many2many(
        "res.groups",
        "extended_security_rule_group_rel",
        "rule_id",
        "group_id",
    )

    perm_read = fields.Boolean("Read")
    perm_write = fields.Boolean("Write")
    perm_create = fields.Boolean("Create")
    perm_unlink = fields.Boolean("Delete")
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        # Clear ORM cache using Odoo 18 registry method
        self.env.registry.clear_cache()
        return res

    def write(self, vals):
        res = super().write(vals)
        self.env.registry.clear_cache()
        return res

    def unlink(self):
        res = super().unlink()
        self.env.registry.clear_cache()
        return res

    @api.model
    def check_user_access(self, model, access_type):
        """Verify if the current user has access to the model for the given operation."""
        for rule in self._iter_matching_rules(model, access_type):
            if not _rule_matches_user(rule, self.env.user):
                raise AccessError(
                    _(
                        "You are not authorized to access records of model {model} "
                        "in {access_type} mode."
                    ).format(model=model, access_type=_(access_type))
                )

    @api.model
    def is_user_authorized(self, model, access_type):
        """Return True if the user is authorized by all matching rules."""
        matching_rules = self._iter_matching_rules(model, access_type)
        return all(_rule_matches_user(rule, self.env.user) for rule in matching_rules)

    @api.model
    def get_user_security_domain(self, model):
        """Return a security domain preventing access to records if unauthorized."""
        authorized = self.is_user_authorized(model, "read")
        return [] if authorized else [("id", "=", False)]

    def _iter_matching_rules(self, model, access_type):
        """Yield rules matching the model and the required access type."""
        rules = self._get_rules()
        return (r for r in rules.get(model, []) if r[access_type])

    @api.model
    @tools.ormcache()
    def _get_rules(self):
        """Fetch and cache all security rules grouped by model name."""
        res = defaultdict(list)
        for record in self.sudo().search([]):
            res[record.model_id.model].append(record._make_rule_dict())
        return res

    def _make_rule_dict(self):
        """Convert rule record to a dictionary."""
        return {
            "group_ids": self.group_ids.ids,
            "read": self.perm_read,
            "write": self.perm_write,
            "create": self.perm_create,
            "unlink": self.perm_unlink,
        }


def _rule_matches_user(rule, user):
    """Return True if the user belongs to at least one group defined in the rule."""
    user_group_ids = user.groups_id.ids
    return any(id_ in user_group_ids for id_ in rule["group_ids"])
