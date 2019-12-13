# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.test_http_request.common import mock_odoo_request
from odoo.addons.base_extended_security.tests.common import (
    ControllerCase,
)
from odoo.addons.base_extended_security.controllers.main import DataSetWithExtendedSecurity


class TestControllers(ControllerCase):

    def setUp(self):
        super().setUp()
        self.controller = DataSetWithExtendedSecurity()

    def _read_grid(self, domain):
        with mock_odoo_request(self.env):
            args = []
            kwargs = {
                'row_fields': ['company_id'],
                'col_field': 'company_id',
                'cell_field': 'company_id',
                'domain': domain,
            }
            return self.controller.call_kw('res.partner', 'read_grid', args, kwargs)

    def test_read_grid_with_empty_domain(self):
        result = self._read_grid([])
        partner_count = result['grid'][0][0]['size']
        assert partner_count == self.customer_count

    def test_read_grid_with_supplier_domain(self):
        result = self._read_grid([('supplier', '=', True)])
        partner_count = result['grid'][0][0]['size']
        assert partner_count == self.supplier_customer_count
