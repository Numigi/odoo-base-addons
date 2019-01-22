# © 2015 Therp BV <https://therp.nl>
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestAuditlogFull(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.accounts_model = cls.env.ref('account.model_account_account')
        cls.accounts_rule = cls.env['auditlog.rule'].create({
            'name': 'Accounts',
            'model_id': cls.accounts_model.id,
            'log_create': True,
            'log_write': True,
            'log_unlink': True,
        })
        cls.name_before = 'Test account 1'
        cls.name_after = 'Test account 2'

        cls.user = cls.env.ref('base.user_demo')
        cls.user.groups_id |= cls.env.ref('account.group_account_manager')

        cls.account = cls.env['account.account'].sudo(cls.user).create({
            'name': cls.name_before,
            'code': '123000',
            'user_type_id': cls.env.ref('account.data_account_type_current_assets').id,
        })

        cls.env['ir.model.access'].create({
            'name': '/',
            'model_id': cls.env.ref('account.model_account_account_tag').id,
            'group_id': cls.env.ref('account.group_account_manager').id,
            'perm_unlink': True,
        })

    def setUp(self):
        super().setUp()
        self.accounts_rule.subscribe()

    def tearDown(self):
        super().tearDown()
        self.accounts_rule.unsubscribe()

    def _find_log(self, account, operation):
        return self.env['auditlog.log'].search([
            ('model_id', '=', self.accounts_model.id),
            ('method', '=', operation),
            ('res_id', '=', account.id),
        ])

    def test_ifRuleIsSubscribed_thenCreateIsLogged(self):
        account = self.env['account.account'].sudo(self.user).create({
            'name': self.name_after,
            'code': '124000',
            'user_type_id': self.env.ref('account.data_account_type_current_assets').id,
        })

        log = self._find_log(account, 'create')
        log.ensure_one()
        line = log.line_ids.filtered(lambda l: l.field_id.name == 'name')
        self.assertFalse(line.old_value)
        self.assertEqual(line.new_value, self.name_after)

    def test_ifRuleIsSubscribed_thenWriteIsLogged(self):
        self.account.name = self.name_after

        log = self._find_log(self.account, 'write')
        log.ensure_one()
        line = log.line_ids.filtered(lambda l: l.field_id.name == 'name')
        self.assertEqual(line.old_value, self.name_before)
        self.assertEqual(line.new_value, self.name_after)

    def test_ifRuleIsSubscribed_thenUnlinkIsLogged(self):
        self.account.unlink()

        log = self._find_log(self.account, 'unlink')
        log.ensure_one()
        line = log.line_ids.filtered(lambda l: l.field_id.name == 'name')
        self.assertFalse(line.old_value)
        self.assertFalse(line.new_value)

    def test_ifRuleIsNotSubscribed_thenCreateIsNotLogged(self):
        self.accounts_rule.unsubscribe()
        account = self.env['account.account'].sudo(self.user).create({
            'name': self.name_after,
            'code': '124000',
            'user_type_id': self.env.ref('account.data_account_type_current_assets').id,
        })

        log = self._find_log(account, 'create')
        self.assertFalse(log)

    def test_ifRuleIsNotSubscribed_thenWriteIsNotLogged(self):
        self.accounts_rule.unsubscribe()
        self.account.name = self.name_after

        log = self._find_log(self.account, 'write')
        self.assertFalse(log)

    def test_ifRuleIsNotSubscribed_thenUnlinkIsNotLogged(self):
        self.accounts_rule.unsubscribe()
        self.account.unlink()

        log = self._find_log(self.account, 'unlink')
        self.assertFalse(log)

    @staticmethod
    def _format_tag_id(tag):
        return "[{tag_id}]".format(tag_id=tag.id, tag_name=tag.display_name)

    @staticmethod
    def _format_tag_text_value(tag):
        return "[({tag_id}, '{tag_name}')]".format(tag_id=tag.id, tag_name=tag.display_name)

    def test_createWithMany2manyField(self):
        tag = self.env.ref('account.account_tag_operating')
        account = self.env['account.account'].sudo(self.user).create({
            'name': self.name_after,
            'code': '124000',
            'user_type_id': self.env.ref('account.data_account_type_current_assets').id,
            'tag_ids': [(4, tag.id)],
        })

        log = self._find_log(account, 'create')
        log.ensure_one()

        log_line = log.line_ids.filtered(lambda l: l.field_id.name == 'tag_ids')
        log_line.ensure_one()

        self.assertFalse(log_line.old_value)
        self.assertEqual(log_line.new_value, self._format_tag_text_value(tag))

    def test_writeWithMany2manyField(self):
        self.accounts_rule.unsubscribe()
        tag_before = self.env.ref('account.account_tag_operating')
        self.account.tag_ids = tag_before
        self.accounts_rule.subscribe()

        tag_after = self.env.ref('account.account_tag_financing')
        self.account.tag_ids = tag_after

        log_line = self._find_log(self.account, 'write').mapped('line_ids')
        log_line.ensure_one()
        self.assertEqual(log_line.old_value, self._format_tag_text_value(tag_before))
        self.assertEqual(log_line.new_value, self._format_tag_text_value(tag_after))

    def test_ifOldx2ManyRecordIsDeleted_thenOldValueTextIsDeleted(self):
        self.accounts_rule.unsubscribe()
        tag_before = self.env.ref('account.account_tag_operating')
        self.account.tag_ids = tag_before
        self.accounts_rule.subscribe()

        tag_after = self.env.ref('account.account_tag_financing')

        value_text_before = "[({tag_id}, 'DELETED')]".format(tag_id=tag_before.id)

        self.account.write({'tag_ids': [(2, tag_before.id), (4, tag_after.id)]})

        log_line = self._find_log(self.account, 'write').mapped('line_ids')
        log_line.ensure_one()
        self.assertEqual(log_line.old_value, value_text_before)
        self.assertEqual(log_line.new_value, self._format_tag_text_value(tag_after))
