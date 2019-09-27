
from odoo import models
from odoo.exceptions import AccessError
from odoo.osv.expression import AND
from odoo.tests.common import SavepointCase


EMPLOYEE_ACCESS_MESSAGE = 'You are not authorized to access employees.'
NON_CUSTOMER_READ_MESSAGE = 'You are not authorized to read non-customers.'
NON_CUSTOMER_WRITE_MESSAGE = 'You are not authorized to edit non-customers.'
NON_CUSTOMER_CREATE_MESSAGE = 'You are not authorized to create non-customers.'
NON_CUSTOMER_UNLINK_MESSAGE = 'You are not authorized to delete non-customers.'


class ResPartner(models.Model):

    _inherit = 'res.partner'

    def get_extended_security_domain(self):
        domain = super().get_extended_security_domain()
        return AND((domain, [('customer', '=', True)]))

    def check_extended_security_all(self):
        super().check_extended_security_all()
        for partner in self:
            if partner.employee:
                raise AccessError(EMPLOYEE_ACCESS_MESSAGE)

    def check_extended_security_read(self):
        super().check_extended_security_read()
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_READ_MESSAGE)

    def check_extended_security_write(self):
        super().check_extended_security_write()
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_WRITE_MESSAGE)

    def check_extended_security_create(self):
        super().check_extended_security_create()
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_CREATE_MESSAGE)

    def check_extended_security_unlink(self):
        super().check_extended_security_unlink()
        for partner in self:
            if not partner.customer:
                raise AccessError(NON_CUSTOMER_UNLINK_MESSAGE)


class ControllerCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env['res.partner'].create({
            'name': 'My Partner Customer',
            'supplier': False,
            'customer': True,
        })
        cls.supplier = cls.env['res.partner'].create({
            'name': 'My Partner Supplier',
            'supplier': True,
            'customer': False,
        })
        cls.supplier_customer = cls.env['res.partner'].create({
            'name': 'My Partner Customer Supplier',
            'supplier': True,
            'customer': True,
        })
        cls.employee = cls.env['res.partner'].create({
            'name': 'My Partner Customer Supplier',
            'supplier': True,
            'customer': True,
            'employee': True,
        })

        cls.customer_count = cls.env['res.partner'].search_count([('customer', '=', True)])
        cls.supplier_customer_count = cls.env['res.partner'].search_count([
            '&', ('customer', '=', True), ('supplier', '=', True),
        ])
