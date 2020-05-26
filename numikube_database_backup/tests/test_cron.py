# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import TransactionCase


class TestBackupCron(TransactionCase):
    def test_backup_file_created(self):
        filenames_before = self._get_filenames()

        self._execute_backup()
        self._check_backups_bucket_exists()

        filenames_after = self._get_filenames()
        assert len(filenames_after) == len(filenames_before) + 1

    def _execute_backup(self):
        cron = self.env.ref("numikube_database_backup.backup_cron")
        cron.method_direct_trigger()

    def _check_backups_bucket_exists(self):
        client = self._get_minio_client()
        assert "backups" in {b.name for b in client.list_buckets()}

    def _get_filenames(self):
        return [f.object_name for f in self._get_objects()]

    def _get_objects(self):
        if self._bucket_exists():
            return self._get_minio_client().list_objects("backups")
        return []

    def _bucket_exists(self):
        client = self._get_minio_client()
        bucket_names = {b.name for b in client.list_buckets()}
        return "backups" in bucket_names

    def _get_minio_client(self):
        return self.env["numikube.database.backup"].get_minio_client()
