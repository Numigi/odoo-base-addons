# Copyright 2022-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo.tests.common import TransactionCase


class TestViewRendering(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.view = cls.env.ref('hr.view_employee_form')

        cls.env = cls.env(user=cls.env.ref('base.user_demo'))
        cls.env.user.groups_id |= cls.env.ref('hr.group_hr_user')
        cls.group = cls.env.ref('private_data_group.group_private_data')
        cls.group.sudo().write({'users': [(3, cls.env.user.id)]})

    def _get_rendered_view_arch(self):
        arch = self.env['hr.employee'].get_view(view_id=self.view.id)['arch']
        return etree.fromstring(arch)

    def test_if_not_authorized__private_field_not_in_view_arch(self):
        #group_private_data=self.env.ref('private_data_group.group_private_data')
        #group_private_data.sudo().write({'users': [(3, self.env.user.id)]})
        arch = self._get_rendered_view_arch()
        assert not arch.xpath("//field[@name='passport_id']")

    def test_if_authorized__private_field_in_view_arch(self):
        self.env.user.groups_id |= self.group
        arch = self._get_rendered_view_arch()
        assert arch.xpath("//field[@name='passport_id']")
