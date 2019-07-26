# © 2019 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import common


class TestMailFollowers(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mail_followers = cls.env['mail.followers']
        cls.main_partner = cls.env['res.partner'].create({'name': 'main'})
        cls.partner1 = cls.env['res.partner'].create({'name': 'toto'})
        cls.partner2 = cls.env['res.partner'].create({'name': 'tata'})
        cls.partner3 = cls.env['res.partner'].create({'name': 'titi'})
        cls.channel1 = cls.env['mail.channel'].create({'name': 'My Channel'})
        cls._insert_partner_follower(cls.partner1)
        cls._insert_partner_follower(cls.partner2)
        cls._insert_partner_follower(cls.partner3)

    @classmethod
    def _insert_partner_follower(cls, partner):
        cls.mail_followers._insert_followers(
            'res.partner', [cls.main_partner.id],
            [partner.id], None,
            [], None,
        )

    @classmethod
    def _insert_channel_follower(cls, channel):
        cls.mail_followers._insert_followers(
            'res.partner', [cls.main_partner.id],
            [], None,
            [channel.id], None,
        )

    def test_when_getRecipientData_thenGetAllPartners(self):
        followers = [f[0] for f in self.mail_followers._get_recipient_data(self.main_partner, 1)]
        assert self.partner1.id in followers
        assert self.partner2.id in followers
        assert self.partner3.id in followers

    def test_when_getRecipientDataWithContext_thenGetSomePartners(self):
        followers = [
            f[0]
            for f in self.mail_followers.with_context(custom_followers=self.partner1)._get_recipient_data(
                self.main_partner, 1
            )
        ]
        assert self.partner1.id in followers
        assert self.partner2.id not in followers
        assert self.partner3.id not in followers

    def _open_mail_compose_wizard(self):
        wizard_obj = (
            self.env['mail.compose.message']
            .with_context(active_id=self.main_partner.id, active_model='res.partner')
        )
        wizard = wizard_obj.create(wizard_obj.default_get(wizard_obj._fields.keys()))
        return wizard

    def test_ifChannelInFollowers_channelIsExcludedFromMailFollowers(self):
        self._insert_channel_follower(self.channel1)
        wizard = self._open_mail_compose_wizard()
        assert wizard.follower_ids == self.partner1 | self.partner2 | self.partner3
