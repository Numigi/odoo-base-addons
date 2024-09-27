# Copyright 2022-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import AccessError
from odoo.osv.expression import AND

PARTNER_ERROR_MESSAGE = _(
    "You are not authorized to access the partner id={} "
    "because it is a private address.",
)


class Partner(models.Model):

    _inherit = 'res.partner'

    def check_extended_security_all(self):
        super().check_extended_security_all()
        for partner in self:
            partner.check_private_address_access()

    def get_extended_security_domain(self):
        result = super().get_extended_security_domain()
        result = AND((result, self.get_private_address_access_domain()))
        return result

    def get_private_address_access_domain(self):
        if self.env.user.has_private_data_access():
            return []
        else:
            return [('type', '!=', 'private')]

    def check_private_address_access(self):
        is_private_address = self.type == 'private'
        if is_private_address and not self.env.user.has_private_data_access():
            raise AccessError(_(PARTNER_ERROR_MESSAGE).format(self.id))
