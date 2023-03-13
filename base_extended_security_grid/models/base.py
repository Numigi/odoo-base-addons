# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from odoo.osv.expression import AND, normalize_domain


class Base(models.AbstractModel):

    _inherit = 'base'

    @api.model
    def read_grid(self, row_fields, col_field, cell_field, domain=None, range=None, readonly_field=None, orderby=None):
        base_domain = normalize_domain(domain)
        security_domain = self.get_extended_security_domain()
        complete_domain = AND((base_domain, security_domain))
        return super().read_grid(row_fields, col_field, cell_field, complete_domain, range, readonly_field, orderby)
