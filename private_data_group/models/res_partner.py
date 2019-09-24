# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, _
from odoo.exceptions import AccessError
from odoo.osv.expression import AND

PARTNER_ERROR_MESSAGE = _(
    "You are not authorized to access the partner id={} "
    "because it is a private address.",
)


SHOW_ADDRESS_CONTEXT_KEYS = {
    'show_address_only',
    'show_address',
    'address_inline',
}


def _check_private_addess_access(partners: 'res.partner'):
    if not partners.env.user.has_private_data_access():
        private_addresses = partners.filtered(lambda p: p.type == 'private')
        if private_addresses:
            context = partners._context
            raise AccessError(_(PARTNER_ERROR_MESSAGE).format(private_addresses[0].id))


class Partner(models.Model):

    _inherit = 'res.partner'

    def check_extended_security_all(self):
        super().check_extended_security_all()
        _check_private_addess_access(self)

    def check_extended_security_name_get(self):
        super().check_extended_security_name_get()
        _check_private_addess_access(self)

    def get_extended_security_domain(self):
        result = super().get_extended_security_domain()

        if not self.env.user.has_private_data_access():
            result = AND((result, [('type', '!=', 'private')]))

        return result
