# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from contextlib import contextmanager
from odoo import SUPERUSER_ID
from odoo.api import Environment
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase
from odoo.sql_db import Cursor, connection_info_for, ConnectionPool
from psycopg2 import ProgrammingError


@contextmanager
def open_cursor(dbname, **kwargs):
    connection_pool = ConnectionPool(1)
    _, dsn = connection_info_for(dbname)
    dsn.update(**kwargs)

    with Cursor(connection_pool, dbname, dsn) as cr:
        yield cr


class BIUserCase(TransactionCase):

    def setUp(self):
        super().setUp()
        self.dbname = self.env.cr.dbname


class TestBIUser(BIUserCase):

    def test_bi_role_exists(self):
        self.env.cr.execute("SELECT 1 FROM pg_roles WHERE rolname='bi'")
        exists = self.env.cr.fetchone()
        assert exists

    def test_if_not_admin__can_not_update_bi_role(self):
        user = self.env.ref('base.user_demo')
        with pytest.raises(AccessError):
            self.env['database.bi.user.update'].sudo(user).setup_role()


class TestBIUserAccess(BIUserCase):

    def setUp(self):
        super().setUp()
        self.password = 'bi_password'
        with open_cursor(self.dbname) as cr:
            cr.execute('ALTER ROLE bi WITH PASSWORD %s', (self.password, ))

    def test_has_select_access_to_odoo_tables(self):
        with open_cursor(self.dbname, user='bi', password=self.password) as cr:
            cr.execute("SELECT count(*) FROM res_partner")
            partner_count = cr.fetchone()
            assert partner_count

    def test_has_not_update_access(self):
        with open_cursor(self.dbname, user='bi', password=self.password) as cr:
            with pytest.raises(ProgrammingError):
                cr.execute("UPDATE res_partner SET name = 'test'")


class TestUpdatePassword(BIUserCase):

    def test_password_is_updated(self):
        new_password = 'my new password'

        with open_cursor(self.dbname) as cr:
            env = Environment(cr, SUPERUSER_ID, {})
            env['database.bi.user.update'].set_password(new_password)

        with open_cursor(self.dbname, user='bi', password=new_password) as cr:
            cr.execute("SELECT count(*) FROM res_partner")
            partner_count = cr.fetchone()
            assert partner_count

    def test_if_not_admin_raise_access_error(self):
        user = self.env.ref('base.user_demo')
        with pytest.raises(AccessError):
            self.env['database.bi.user.update'].sudo(user).set_password('new_password')
