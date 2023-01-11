# © 2023 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from ddt import ddt, data, unpack
from odoo.tests import common


@ddt
class TestSelectionLabel(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fr = cls.env['res.lang'].with_context(active_test=False).search([
            ('code', '=', 'fr_FR'),
        ])

    @data(
        ('1', "Monday"),
        ('2', "Tuesday"),
    )
    @unpack
    def test_get_selection_label(self, week_start, label):
        self.fr.week_start = week_start
        lang = self.fr.with_context(lang="en_US")
        assert lang.get_selection_label("week_start") == label
