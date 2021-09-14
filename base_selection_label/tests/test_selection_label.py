# © 2021 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestSelectionLabel(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fr = cls.env['res.lang'].with_context(active_test=False).search([
            ('code', '=', 'fr_FR'),
        ])
        cls.fr.week_start = 1

    def test_get_selection_label(self):
        lang = self.fr.with_context(lang="en_US")
        label = lang.get_selection_label("week_start")
        assert label == "Monday"
