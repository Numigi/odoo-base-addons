# © 2022 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from lxml import etree
from ddt import ddt, data, unpack
from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase


@ddt
class TestSecurityRules(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = cls.env["res.groups"].create(
            {
                "name": "My User Group",
            }
        )

        cls.user = cls.env["res.users"].create(
            {
                "name": "test@example.com",
                "login": "test@example.com",
                "email": "test@example.com",
                "groups_id": [(4, cls.env.ref("base.group_user").id)],
            }
        )

        cls.product = cls.env["product.product"].create(
            {
                "name": "Product 1",
            }
        )

        cls.rule = cls.env["extended.security.rule"].create(
            {
                "model_id": cls.env.ref("product.model_product_product").id,
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
        getattr(self.product.with_user(self.user), method)()

    @data("read", "write", "create", "unlink")
    def test_if_access_type_uncheked__access_error_raised(self, access_type):
        method = "check_extended_security_{}".format(access_type)
        getattr(self.product.with_user(self.user), method)()

    @data("read", "write", "create", "unlink")
    def test_if_not_member_of_group__access_error_raised(self, access_type):
        self.rule["perm_{}".format(access_type)] = True

        method = "check_extended_security_{}".format(access_type)
        with pytest.raises(AccessError):
            getattr(self.product.with_user(self.user), method)()

    def test_after_rule_deleted__rule_not_applied(self):
        self.rule.perm_read = True

        with pytest.raises(AccessError):
            self.product.with_user(self.user).check_extended_security_read()

        self.rule.unlink()
        self.product.with_user(self.user).check_extended_security_read()

    def test_after_rule_created__rule_applied(self):
        self.product.with_user(self.user).check_extended_security_read()

        self.rule.copy({"perm_read": True})

        with pytest.raises(AccessError):
            self.product.with_user(self.user).check_extended_security_read()

    def test_after_rule_unchecked__rule_not_applied(self):
        self.rule.perm_read = True

        with pytest.raises(AccessError):
            self.product.with_user(self.user).check_extended_security_read()

        self.rule.perm_read = False

        self.product.with_user(self.user).check_extended_security_read()

    def test_after_rule_archived__rule_not_applied(self):
        self.rule.perm_read = True

        with pytest.raises(AccessError):
            self.product.with_user(self.user).check_extended_security_read()

        self.rule.active = False

        self.product.with_user(self.user).check_extended_security_read()

    def test_after_rule_checked__rule_applied(self):
        self.product.with_user(self.user).check_extended_security_read()

        self.rule.perm_read = True

        with pytest.raises(AccessError):
            self.product.with_user(self.user).check_extended_security_read()

    def test_on_search__if_not_authorized__domain_is_empty(self):
        self.rule.perm_read = True

        domain = (
            self.env["product.product"].with_user(self.user).get_extended_security_domain()
        )
        search_result = self.env["product.product"].search(domain)

        assert self.product not in search_result

    def test_on_search__if_authorized__domain_not_empty(self):
        self.rule.perm_read = True
        self.user.groups_id |= self.group

        domain = (
            self.env["product.product"].with_user(self.user).get_extended_security_domain()
        )
        search_result = self.env["product.product"].search(domain)

        assert self.product in search_result

    def _get_product_list_view_arch(self):
        view = self.env.ref("product.product_product_tree_view")
        arch = self.env["product.product"].fields_view_get(view_id=view.id)["arch"]
        return etree.fromstring(arch)

    @data(
        ("write", "edit"),
        ("create", "create"),
        ("unlink", "delete"),
    )
    @unpack
    def test_if_unauthorized__view_property_disabled(self, access_type, view_property):
        self.rule["perm_{}".format(access_type)] = True

        list_view = self._get_product_list_view_arch()
        assert list_view.attrib[view_property] == "false"

    @data(
        ("write", "edit"),
        ("create", "create"),
        ("unlink", "delete"),
    )
    @unpack
    def test_if_authorized__view_property_not_disabled(
        self, access_type, view_property
    ):
        list_view = self._get_product_list_view_arch()
        assert view_property not in list_view.attrib

    def _get_nested_ir_rule_many2many_arch(self):
        view = self.env.ref("base.view_groups_form")
        result = self.env["res.groups"].fields_view_get(view_id=view.id)
        arch = result["fields"]["rule_groups"]["views"]["tree"]["arch"]
        return etree.fromstring(arch)

    @data(
        ("write", "edit"),
        ("create", "create"),
        ("unlink", "delete"),
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
        many2many_list = self._get_nested_ir_rule_many2many_arch()
        assert view_property not in many2many_list.attrib

    def _get_nested_ir_model_access_one2many_arch(self):
        view = self.env.ref("base.view_groups_form")
        result = self.env["res.groups"].fields_view_get(view_id=view.id)
        arch = result["fields"]["model_access"]["views"]["tree"]["arch"]
        return etree.fromstring(arch)

    @data(
        ("write", "edit"),
        ("create", "create"),
        ("unlink", "delete"),
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
            }
        )
        one2many_list = self._get_nested_ir_model_access_one2many_arch()
        assert view_property in one2many_list.attrib

    def test_if_authorized__toggle_button_not_hidden(self):
        form_view = self._get_product_form_view_arch()
        assert form_view.xpath("//button[@name='toggle_active']")

    def test_if_not_authorized__toggle_button_hidden(self):
        self.rule.perm_write = True

        form_view = self._get_product_form_view_arch()
        assert not form_view.xpath("//button[@name='toggle_active']")

    def test_if_not_authorized__action_buttons_still_visible(self):
        self.env.user.groups_id |= self.env.ref("product.group_product_variant")
        form_view = self._get_product_form_view_arch()
        action = self.env.ref("product.product_attribute_value_action")
        assert form_view.xpath("//button[@name='{}']".format(action.id))

    def test_read_access_action(self):
        self.rule.model_id = self.env.ref("base.model_res_partner")
        self.rule.perm_write = True
        form_view = self._get_partner_form_view_arch()
        assert form_view.xpath("//button[@name='create_company']")

    def _get_product_form_view_arch(self):
        return self._get_form_view_arch(
            "product.product", "product.product_normal_form_view"
        )

    def _get_partner_form_view_arch(self):
        return self._get_form_view_arch("res.partner", "base.view_partner_form")

    def _get_form_view_arch(self, model, view_ref):
        view = self.env.ref(view_ref)
        arch = self.env[model].fields_view_get(view_id=view.id)["arch"]
        return etree.fromstring(arch)
