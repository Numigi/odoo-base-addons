# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.tests import common
from odoo.exceptions import AccessError


class TestResPartner(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.private_address = cls.env['res.partner'].create({
            'name': 'Private Address',
            'type': 'private',
        })

        cls.contact = cls.env['res.partner'].create({
            'name': 'Contact',
            'type': 'contact',
        })

        cls.user = cls.env.ref('base.user_demo')
        cls.user.groups_id |= cls.env.ref('hr.group_hr_user')

        cls.group = cls.env.ref('private_data_group.group_private_data')

    def test_if_is_authorized__access_error_not_raised(self):
        self.user.groups_id |= self.group
        self.private_address.sudo(self.user).check_extended_security_all()

    def test_if_partner_is_not_private__access_error_not_raised(self):
        self.contact.sudo(self.user).check_extended_security_all()

    def test_if_not_authorized__access_error_raised(self):
        with pytest.raises(AccessError):
            self.private_address.sudo(self.user).check_extended_security_all()

    def test_if_is_authorized__access_error_not_raised_on_name_get(self):
        self.user.groups_id |= self.group
        self.private_address.sudo(self.user).check_extended_security_name_get()

    def test_if_partner_is_not_private__access_error_not_raised_on_name_get(self):
        self.contact.sudo(self.user).check_extended_security_name_get()

    def test_if_not_authorized__access_error_raised_on_name_get(self):
        with pytest.raises(AccessError):
            self.private_address.sudo(self.user).check_extended_security_name_get()

    def _search_partners(self):
        partner_pool = self.env['res.partner'].sudo(self.user)
        domain = partner_pool.get_extended_security_domain()
        return partner_pool.search(domain)

    def test_if_is_authorized__private_address_searchable(self):
        self.user.groups_id |= self.group
        assert self.private_address in self._search_partners()

    def test_non_private_partners_searchable(self):
        assert self.contact in self._search_partners()

    def test_if_not_authorized__private_address_not_searchable(self):
        assert self.private_address not in self._search_partners()
