# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestRenameMenuItem(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fr_lang = cls.env['res.lang'].with_context(active_test=False).search([
            ('code', '=', 'fr_FR'),
        ])
        cls.fr_lang.active = True

        cls.menu_name_en = 'Settings'
        cls.menu_name_fr = 'Configuration'
        cls.menu = cls.env.ref('base.menu_administration')
        cls.menu.with_context(lang='fr_FR').name = cls.menu_name_fr

    def _rename_menu(self, lang, label):
        self.env['ir.ui.menu'].rename('base.menu_administration', lang, label)

    def test_after_rename_menu_with_fr__fr_translation_updated(self):
        new_label = 'Nouveau libellé'
        self._rename_menu('fr_FR', new_label)
        assert self.menu.with_context(lang='fr_FR').name == new_label

    def test_after_rename_menu_with_fr__en_translation_unchanged(self):
        new_label = 'Nouveau libellé'
        self._rename_menu('fr_FR', new_label)
        assert self.menu.with_context(lang='en_US').name == self.menu_name_en

    def test_after_rename_menu_with_en__en_translation_updated(self):
        new_label = 'New label'
        self._rename_menu('en_US', new_label)
        assert self.menu.with_context(lang='en_US').name == new_label

    def test_after_rename_menu_with_en__fr_translation_unchanged(self):
        new_label = 'New label'
        self._rename_menu('en_US', new_label)
        assert self.menu.with_context(lang='fr_FR').name == self.menu_name_fr
