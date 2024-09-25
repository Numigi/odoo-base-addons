
from odoo import models, api
from odoo.exceptions import AccessError
from odoo.osv.expression import AND
from odoo.tests.common import TransactionCase


EMPLOYEE_ACCESS_MESSAGE = 'You are not authorized to access employees.'
NON_CUSTOMER_READ_MESSAGE = 'You are not authorized to read non-customers.'
NON_CUSTOMER_WRITE_MESSAGE = 'You are not authorized to edit non-customers.'
NON_CUSTOMER_CREATE_MESSAGE = 'You are not authorized to create non-customers.'
NON_CUSTOMER_UNLINK_MESSAGE = 'You are not authorized to delete non-customers.'


class ResPartner(models.Model):

    _inherit = 'res.partner'

    def get_extended_security_domain(self):
        domain = super().get_extended_security_domain()
        return AND((domain, [('customer_rank', '>', 0)]))

    def check_extended_security_all(self):
        super().check_extended_security_all()
        for partner in self:
            if partner.employee:
                raise AccessError(EMPLOYEE_ACCESS_MESSAGE)

    def check_extended_security_read(self):
        super().check_extended_security_read()
        for partner in self:
            if partner.customer_rank < 1:
                raise AccessError(NON_CUSTOMER_READ_MESSAGE)

    def check_extended_security_write(self):
        super().check_extended_security_write()
        for partner in self:
            if partner.customer_rank < 1:
                raise AccessError(NON_CUSTOMER_WRITE_MESSAGE)

    def check_extended_security_create(self):
        super().check_extended_security_create()
        for partner in self:
            if partner.customer_rank < 1:
                raise AccessError(NON_CUSTOMER_CREATE_MESSAGE)

    def check_extended_security_unlink(self):
        super().check_extended_security_unlink()
        for partner in self:
            if partner.customer_rank < 1:
                raise AccessError(NON_CUSTOMER_UNLINK_MESSAGE)

    @api.model
    def get_read_access_actions(self):
        res = super().get_read_access_actions()
        res.append("create_company")
        return res


class ControllerCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer = cls.env['res.partner'].create({
            'name': 'My Partner Customer',
            'supplier_rank': 0,
            'customer_rank': 1,
        })
        cls.supplier = cls.env['res.partner'].create({
            'name': 'My Partner Supplier',
            'supplier_rank': 1,
            'customer_rank': 0,
        })
        cls.supplier_customer = cls.env['res.partner'].create({
            'name': 'My Partner Customer Supplier',
            'supplier_rank': 1,
            'customer_rank': 1,
        })
        cls.employee = cls.env['res.partner'].create({
            'name': 'My Partner Customer Supplier',
            'supplier_rank': 1,
            'customer_rank': 1,
            'employee': True,
        })

        cls.customer_count = cls.env['res.partner'].search_count([('customer_rank', '>', 0)])
        cls.supplier_customer_count = cls.env['res.partner'].search_count([
            '&', ('customer_rank', '>', 0), ('supplier_rank', '>', 0),
        ])
