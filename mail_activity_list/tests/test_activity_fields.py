# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta

from odoo import fields
from odoo.tests import common


class TestActivityFields(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test'})
        cls.date_deadline = datetime.now().date() - timedelta(10)
        cls.activity = cls.env['mail.activity'].create({
            'res_id': cls.partner.id,
            'res_model_id': cls.env.ref('base.model_res_partner').id,
            'date_deadline': cls.date_deadline,
            'user_id': cls.env.user.id,
        })

    def test_if_not_archived__effective_date_is_date_deadline(self):
        expected_date = fields.Date.to_string(self.date_deadline)
        assert self.activity.effective_date == expected_date

    def test_if_archived__effective_date_is_date_done(self):
        expected_date = fields.Date.to_string(datetime.now().date())
        self.activity.action_done()
        assert self.activity.effective_date == expected_date

    def test_record_reference(self):
        assert self.activity.record_reference == "res.partner,{}".format(self.partner.id)

    def test_if_activity_has_no_summary__display_name_is_activity(self):
        self.env.user.lang = 'en_US'
        assert self.activity.display_name == 'Activity'

    def test_if_activity_has_summary__display_name_is_summary(self):
        self.activity.summary = 'Test'
        assert self.activity.display_name == 'Test'
