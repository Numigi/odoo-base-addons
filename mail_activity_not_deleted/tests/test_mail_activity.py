# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from odoo import fields
from odoo.tests import common


class TestMailActivity(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test'})
        cls.activity = cls.env['mail.activity'].create({
            'res_id': cls.partner.id,
            'res_model_id': cls.env.ref('base.model_res_partner').id,
            'date_deadline': datetime.now().date(),
            'user_id': cls.env.user.id,
        })
        cls.partner.modified(['activity_ids'])
        cls.partner.recompute()

    def test_when_activity_is_completed_then_it_is_inactive_instead_of_deleted(self):
        self.assertTrue(self.activity.active)

        self.activity.action_done()
        self.assertTrue(self.activity.exists())
        self.assertFalse(self.activity.active)

    def test_when_record_is_deactivated_then_the_activity_is_inactive_instead_of_deleted(self):
        self.assertTrue(self.activity.active)

        self.partner.active = False
        self.activity.refresh()
        self.assertTrue(self.activity.exists())
        self.assertFalse(self.activity.active)

    def test_the_date_done_is_computed_when_the_activity_is_completed(self):
        self.assertFalse(self.activity.date_done)

        time_before = fields.Datetime.to_string(datetime.now())
        self.activity.action_done()
        time_after = fields.Datetime.to_string(datetime.now())

        self.assertLessEqual(time_before, self.activity.date_done)
        self.assertLessEqual(self.activity.date_done, time_after)

    def test_the_state_is_done_after_the_activity_is_completed(self):
        self.assertNotEqual(self.activity.state, 'done')
        self.activity.action_done()
        self.activity.refresh()
        self.assertEqual(self.activity.state, 'done')

    def test_when_the_activity_is_archived_then_it_is_not_due_today(self):
        self.assertEqual(self.partner.activity_state, 'today')
        self.activity.action_done()
        self.assertFalse(self.partner.activity_state)

    def test_when_the_activity_is_archived_then_partner_has_no_activity_deadline(self):
        self.assertTrue(self.partner.activity_date_deadline)
        self.activity.action_done()
        self.assertFalse(self.partner.activity_date_deadline)
