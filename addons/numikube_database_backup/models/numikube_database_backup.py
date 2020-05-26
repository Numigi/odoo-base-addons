# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import tempfile
from datetime import datetime
from minio import Minio
from odoo.models import AbstractModel
from odoo.service.db import dump_db


BUCKET_NAME = "backups"


class DatabaseBackup(AbstractModel):

    _name = "numikube.database.backup"
    _description = "Numikube Database Backup"

    def run_backup(self):
        self._autocreate_backups_bucket()
        self._execute_backup()

    def get_minio_client(self):
        return Minio(
            "minio:9000",
            access_key="minio",
            secret_key="miniosecret",
            secure=False,
        )

    def _autocreate_backups_bucket(self):
        client = self.get_minio_client()
        bucket_names = {b.name for b in client.list_buckets()}
        if BUCKET_NAME not in bucket_names:
            client.make_bucket(BUCKET_NAME, location="us-east-1")

    def _execute_backup(self):
        filename = self._make_filename()

        with tempfile.NamedTemporaryFile() as file:
            dump_db(self._database_name, file, "dump")
            self._transfer_file_to_minio(filename, file)

    def _transfer_file_to_minio(self, filename, file):
        client = self.get_minio_client()
        client.fput_object(BUCKET_NAME, filename, file.name)

    def _make_filename(self):
        return "{:%Y_%m_%d_%H_%M_%S}.dump".format(datetime.now())

    @property
    def _database_name(self):
        return self.env.cr.dbname
