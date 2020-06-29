# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import tempfile
from datetime import datetime
from minio import Minio
from odoo.models import AbstractModel
from odoo.service.db import dump_db
from odoo.addons.numikube_minio.minio import get_minio_client, auto_create_bucket
from ..bucket import get_backups_bucket_name


class DatabaseBackup(AbstractModel):

    _name = "numikube.database.backup"
    _description = "Numikube Database Backup"

    def run_backup(self):
        self._autocreate_backups_bucket()
        self._execute_backup()

    def _autocreate_backups_bucket(self):
        bucket_name = get_backups_bucket_name()
        auto_create_bucket(bucket_name)

    def _execute_backup(self):
        filename = self._make_filename()

        with tempfile.NamedTemporaryFile() as file:
            dump_db(self._database_name, file, "dump")
            self._transfer_file_to_minio(filename, file)

    def _transfer_file_to_minio(self, filename, file):
        client = get_minio_client()
        bucket_name = get_backups_bucket_name()
        client.fput_object(bucket_name, filename, file.name)

    def _make_filename(self):
        return "{:%Y_%m_%d_%H_%M_%S}.dump".format(datetime.now())

    @property
    def _database_name(self):
        return self.env.cr.dbname
