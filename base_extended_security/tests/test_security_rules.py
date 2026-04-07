# Copyright 2024-today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from lxml import etree
from ddt import ddt, data, unpack
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


@ddt
class TestSecurityRules(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = cls.env["res.groups"].create({"name": "My User Group"})

        cls.user = cls.env["res.users"].create(
            {
                "name": "test@example.com",
                "login": "test@example.com",
                "email": "test@example.com",
                "groups_id": [
                    (4, cls.env.ref("base.group_user").id),
                    (4, cls.env.ref("base.group_system").id),
                ],
            }
        )

        # IMPORTANT: Setting color=1 to bypass the non-customer restriction from common.py
        cls.partner = cls.env["res.partner"].create({"name": "Partner 1", "color": 1})

        cls.rule = cls.env["extended.security.rule"].create(
            {
                "model_id": cls.env.ref("base.model_res_partner").id,
                "group_ids": [(4, cls.group.id)],
                "perm_read": False,
                "perm_write": False,
                "perm_create": False,
                "perm_unlink": False,
            }
        )

        cls.res_partner_model = cls.env["ir.model"].search(
            [("model", "=", "res.partner")]
        )
        cls.comment_html = "<p>MyComment</p>"
        cls.action_1 = cls.env["ir.actions.server"].create(
            {
                "name": "TestAction",
                "model_id": cls.res_partner_model.id,
                "state": "code",
                "code": 'record.write({"comment": "%s"})' % cls.comment_html,
            }
        )
        cls.rule_1 = cls.env["extended.security.rule"].create(
            {
                "model_id": cls.env.ref("base.model_ir_actions_server").id,
                "group_ids": [(4, cls.group.id)],
                "perm_read": False,
                "perm_write": False,
                "perm_create": False,
                "perm_unlink": False,
            }
        )

    @data("read", "write", "create", "unlink")
    def test_if_member_of_group__access_error_not_raised(self, access_type):
        self.rule["perm_{}".format(access_type)] = True
        self.user.groups_id |= self.group
        method = "check_extended_security_{}".format(access_type)
        getattr(self.partner.with_user(self.user), method)()

    @data("read", "write", "create", "unlink")
    def test_if_access_type_uncheked__access_error_raised(self, access_type):
        method = "check_extended_security_{}".format(access_type)
        getattr(self.partner.with_user(self.user), method)()

    @data("read", "write", "create", "unlink")
    def test_if_not_member_of_group__access_error_raised(self, access_type):
        self.rule["perm_{}".format(access_type)] = True
        method = "check_extended_security_{}".format(access_type)

        with pytest.raises(AccessError):
            getattr(self.partner.with_user(self.user), method)()

    def test_after_rule_deleted__rule_not_applied(self):
        self.rule.perm_read = True
        with pytest.raises(AccessError):
            self.partner.with_user(self.user).check_extended_security_read()

        self.rule.unlink()
        self.partner.with_user(self.user).check_extended_security_read()

    def test_after_rule_created__rule_applied(self):
        self.partner.with_user(self.user).check_extended_security_read()
        self.rule.copy({"perm_read": True})

        with pytest.raises(AccessError):
            self.partner.with_user(self.user).check_extended_security_read()

    def test_after_rule_unchecked__rule_not_applied(self):
        self.rule.perm_read = True
        with pytest.raises(AccessError):
            self.partner.with_user(self.user).check_extended_security_read()

        self.rule.perm_read = False
        self.partner.with_user(self.user).check_extended_security_read()

    def test_after_rule_archived__rule_not_applied(self):
        self.rule.perm_read = True
        with pytest.raises(AccessError):
            self.partner.with_user(self.user).check_extended_security_read()

        self.rule.active = False
        self.partner.with_user(self.user).check_extended_security_read()

    def test_after_rule_checked__rule_applied(self):
        self.partner.with_user(self.user).check_extended_security_read()

        self.rule.perm_read = True
        with pytest.raises(AccessError):
            self.partner.with_user(self.user).check_extended_security_read()

    def test_on_search__if_not_authorized__domain_is_empty(self):
        self.rule.perm_read = True
        domain = (
            self.env["res.partner"].with_user(self.user).get_extended_security_domain()
        )
        search_result = self.env["res.partner"].search(domain)
        assert self.partner not in search_result

    def test_on_search__if_authorized__domain_not_empty(self):
        self.rule.perm_read = True
        self.user.groups_id |= self.group
        domain = (
            self.env["res.partner"].with_user(self.user).get_extended_security_domain()
        )
        search_result = self.env["res.partner"].search(domain)
        assert self.partner in search_result

    def _get_partner_list_view_arch(self):
        view = self.env.ref("base.view_partner_tree")
        arch = (
            self.env["res.partner"]
            .with_user(self.user)
            .get_view(view_id=view.id, view_type="list")["arch"]
        )
        return etree.fromstring(arch)

    def _get_nested_field_node(self, model, view_ref, field_name):
        view = self.env.ref(view_ref)
        arch = (
            self.env[model]
            .with_user(self.user)
            .get_view(view_id=view.id, view_type="form")["arch"]
        )
        tree = etree.fromstring(arch)
        return tree.xpath(f"//field[@name='{field_name}']")[0]

    @data(
        ("write", "edit"),
        ("create", "create"),
        ("unlink", "delete"),
    )
    @unpack
    def test_if_authorized__view_property_not_disabled(
        self, access_type, view_property
    ):
        self.user.groups_id |= self.group
        self.rule["perm_{}".format(access_type)] = True
        list_view = self._get_partner_list_view_arch()
        assert list_view.attrib.get(view_property) != "false"

    @data(
        ("write", "can_write"),
        ("create", "can_create"),
    )
    @unpack
    def test_in_nested_many2many_list__view_property_not_disabled(
        self, access_type, view_property
    ):
        self.env["extended.security.rule"].create(
            {
                "model_id": self.env.ref("base.model_ir_rule").id,
                "group_ids": [(4, self.group.id)],
                "perm_{}".format(access_type): True,
            }
        )
        self.user.groups_id |= self.group
        field_node = self._get_nested_field_node(
            "res.groups", "base.view_groups_form", "rule_groups"
        )
        assert field_node.attrib.get(view_property) != "False"

    def test_if_not_authorized__toggle_button_hidden(self):
        self.rule_1.perm_write = True
        form_view = self._get_ir_actions_server_form_view_arch()
        assert not form_view.xpath("//header/button[@name='create_action']")

    def test_if_authorized__toggle_button_not_hidden(self):
        self.user.groups_id |= self.group
        form_view = self._get_ir_actions_server_form_view_arch()
        assert form_view.xpath("//header/button[@name='create_action']")

    @data(
        ("write", "edit"),
        ("create", "create"),
    )
    @unpack
    def test_in_nested_one2many_list__view_property_disabled(
        self, access_type, view_property
    ):
        self.env["extended.security.rule"].create(
            {
                "model_id": self.env.ref("base.model_ir_model_access").id,
                "group_ids": [(4, self.group.id)],
                "perm_{}".format(access_type): True,
                "active": True,
            }
        )
        field_node = self._get_nested_field_node(
            "res.groups", "base.view_groups_form", "model_access"
        )
        list_node = field_node.xpath(".//list")[0]
        assert list_node.attrib.get(view_property) == "false"

    def test_read_access_action(self):
        self.rule.model_id = self.env.ref("base.model_res_partner")
        self.rule.perm_write = True
        form_view = self._get_partner_form_view_arch()
        assert form_view.xpath("//field[@name='vat']")

    @data(
        ("write", "edit"),
        ("create", "create"),
        ("unlink", "delete"),
    )
    @unpack
    def test_if_unauthorized__view_property_disabled(self, access_type, view_property):
        self.rule["perm_{}".format(access_type)] = True
        list_view = self._get_partner_list_view_arch()
        assert list_view.attrib.get(view_property) == "false"

    def _get_partner_form_view_arch(self):
        return self._get_form_view_arch("res.partner", "base.view_partner_form")

    def _get_ir_actions_server_form_view_arch(self):
        return self._get_form_view_arch(
            "ir.actions.server", "base.view_server_action_form"
        )

    def _get_form_view_arch(self, model, view_ref):
        view = self.env.ref(view_ref)
        arch = (
            self.env[model]
            .with_user(self.user)
            .get_view(view_id=view.id, view_type="form")["arch"]
        )
        return etree.fromstring(arch)

    def test_if_authorized__field_not_hidden(self):
        self.user.groups_id |= self.group
        form_view = self._get_partner_form_view_arch()
        assert form_view.xpath("//field[@name='name']")
