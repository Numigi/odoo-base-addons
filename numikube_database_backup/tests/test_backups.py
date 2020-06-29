# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import TransactionCase
from odoo.addons.numikube_minio.minio import get_minio_client, get_bucket_names


class TestBackups(TransactionCase):
    def test_backup(self):
        filenames_before = self._get_filenames()

        self._execute_backup()
        assert self._bucket_exists()

        filenames_after = self._get_filenames()
        assert len(filenames_after) == len(filenames_before) + 1

    def _execute_backup(self):
        cron = self.env.ref("numikube_database_backup.backup_cron")
        cron.method_direct_trigger()

    def _get_filenames(self):
        return [f.object_name for f in self._get_objects()]

    def _get_objects(self):
        if self._bucket_exists():
            return get_minio_client().list_objects("dev-backups")
        return []

    def _bucket_exists(self):
        return "dev-backups" in get_bucket_names()
