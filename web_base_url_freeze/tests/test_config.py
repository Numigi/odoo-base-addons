
from odoo.tests import TransactionCase


class TestConfig(TransactionCase):

    def test_web_base_url_freeze(self):
        self.assertTrue(self.env['ir.config_parameter'].sudo().get_param('web.base.url.freeze'))
