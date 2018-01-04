import logging

from odoo.tests import common
logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    """Use case of creation of a partner."""
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.country_pool = self.env['res.country']
        self.canada = self.country_pool.browse(39)

    def test_create(self):
        name = 'tpartner'
        partner = self.partner_pool.create({
            'name': name,
            'state_id': 1,
            'country_id': self.canada.id,
        })
        self.assertEqual(name, partner.name)
