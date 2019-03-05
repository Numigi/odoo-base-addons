# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestNoteNoDefaultStage(common.TransactionCase):

    def test_on_create_user__no_default_stage(self):
        email = 'test-no-default-stage@example.com'
        new_user = self.env['res.users'].create({
            'name': email,
            'login': email,
            'email': email,
        })
        stages = self.env['note.stage'].search([('user_id', '=', new_user.id)])
        assert not stages
