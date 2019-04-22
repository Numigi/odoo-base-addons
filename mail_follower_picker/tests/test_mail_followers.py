# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestMailFollowers(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mail_followers = cls.env['mail.followers']
        cls.main_partner = cls.env['res.partner'].create({'name': 'main'})
        cls.partner1 = cls.env['res,partner'].create({'name': 'toto'})
        cls.partner2 = cls.env['res,partner'].create({'name': 'tata'})
        cls.partner3 = cls.env['res,partner'].create({'name': 'titi'})

        cls.mail_followers._insert_followers(
            'res.partner',
            [cls.main_partner.id],
            [cls.partner1.id, cls.partner2.id, cls.partner3.id],
            None, None, None
        )

    def test_when_getRecipientData_thenGetAllPartners(self):
        followers = [f[0] for f in self.mail_followers._get_recipient_data(self.main_partner, 1)]
        assert self.partner1 in followers
        assert self.partner2 in followers
        assert self.partner3 in followers

    def test_when_getRecipientDataWithContext_thenGetSomePartners(self):
        followers = [
            f[0]
            for f in self.mail_followers.with_context(custom_followers=[self.partner1])._get_recipient_data(
                self.main_partner, 1
            )
        ]
        assert self.partner1 in followers
        assert not self.partner2 in followers
        assert not self.partner3 in followers
