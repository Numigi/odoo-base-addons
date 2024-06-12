# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime
from odoo.tests.common import TransactionCase
from odoo.addons.numikube_minio.minio import get_minio_client, get_bucket_names


class TestBackups(TransactionCase):
    def setUp(self):
        super().setUp()
        self.db_name = self.env.cr.dbname

    def test_hourly_backup(self):
        self._execute_hourly_backup()
        filenames = self._get_filenames()
        backup_number = datetime.now().hour % 3
        expected_filename = "{db_name}-hourly-{backup_number}.dump".format(
            db_name=self.db_name, backup_number=backup_number
        )
        assert expected_filename in filenames

    def test_daily_backup(self):
        self._execute_daily_backup()
        filenames = self._get_filenames()
        backup_number = datetime.now().isoweekday()
        expected_filename = "{db_name}-daily-{backup_number}.dump".format(
            db_name=self.db_name, backup_number=backup_number
        )
        assert expected_filename in filenames

    def _execute_hourly_backup(self):
        cron = self.env.ref("numikube_database_backup.backup_cron")
        cron.method_direct_trigger()

    def _execute_daily_backup(self):
        cron = self.env.ref("numikube_database_backup.daily_backup_cron")
        cron.method_direct_trigger()

    def _get_filenames(self):
        return [f.object_name for f in self._get_objects()]

    def _get_objects(self):
        if self._bucket_exists():
            return get_minio_client().list_objects("dev-backups")
        return []

    def _bucket_exists(self):
        return "dev-backups" in get_bucket_names()
