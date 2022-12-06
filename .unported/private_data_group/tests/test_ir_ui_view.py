# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo.tests import common


class TestViewRendering(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.view = cls.env.ref('hr.view_employee_form')

        cls.env = cls.env(user=cls.env.ref('base.user_demo'))
        cls.env.user.groups_id |= cls.env.ref('hr.group_hr_user')

    def _get_rendered_view_arch(self):
        arch = self.env['hr.employee'].fields_view_get(view_id=self.view.id)['arch']
        return etree.fromstring(arch)

    def test_if_not_authorized__private_field_not_in_view_arch(self):
        arch = self._get_rendered_view_arch()
        assert not arch.xpath("//field[@name='passport_id']")

    def test_if_authorized__private_field_in_view_arch(self):
        self.env.user.groups_id |= self.env.ref('private_data_group.group_private_data')
        arch = self._get_rendered_view_arch()
        assert arch.xpath("//field[@name='passport_id']")
