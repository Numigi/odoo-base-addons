# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestRenamegroupItem(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.fr_lang = cls.env['res.lang'].with_context(active_test=False).search([
            ('code', '=', 'fr_FR'),
        ])
        cls.fr_lang.active = True

        cls.group_name_en = 'Access Rights'
        cls.group_name_fr = "Droits d'accès"
        cls.group = cls.env.ref('base.group_erp_manager')
        cls.group.with_context(lang='fr_FR').name = cls.group_name_fr

    def _rename_group(self, lang, label):
        self.env['res.groups'].rename('base.group_erp_manager', lang, label)

    def test_after_rename_group_with_fr__fr_translation_updated(self):
        new_label = 'Nouveau libellé'
        self._rename_group('fr_FR', new_label)
        assert self.group.with_context(lang='fr_FR').name == new_label

    def test_after_rename_group_with_fr__en_translation_unchanged(self):
        new_label = 'Nouveau libellé'
        self._rename_group('fr_FR', new_label)
        assert self.group.with_context(lang='en_US').name == self.group_name_en

    def test_after_rename_group_with_en__en_translation_updated(self):
        new_label = 'New label'
        self._rename_group('en_US', new_label)
        assert self.group.with_context(lang='en_US').name == new_label

    def test_after_rename_group_with_en__fr_translation_unchanged(self):
        new_label = 'New label'
        self._rename_group('en_US', new_label)
        assert self.group.with_context(lang='fr_FR').name == self.group_name_fr

    def test_if_lang_not_active__term_ignored(self):
        self.fr_lang.active = False
        self._rename_group('fr_FR', 'Nouveau libellé')
        assert self.group.name == self.group_name_en
