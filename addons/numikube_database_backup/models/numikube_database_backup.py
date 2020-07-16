# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import tempfile
import logging
from datetime import datetime
from minio import Minio
from odoo.models import AbstractModel
from odoo.service.db import dump_db
from odoo.addons.numikube_minio.minio import get_minio_client, auto_create_bucket
from ..bucket import get_backups_bucket_name

_logger = logging.getLogger(__name__)


class DatabaseBackup(AbstractModel):

    _name = "numikube.database.backup"
    _description = "Numikube Database Backup"

    def run_backup(self):
        """Run a backup.

        .. deprecated:: 1.1.0

        Method kept for backward compatibility.
        """
        self.run_hourly_backup()

    def run_hourly_backup(self):
        self._autocreate_backups_bucket()
        self._execute_hourly_backup()

    def run_daily_backup(self):
        self._autocreate_backups_bucket()
        self._execute_daily_backup()

    def _autocreate_backups_bucket(self):
        bucket_name = get_backups_bucket_name()
        auto_create_bucket(bucket_name)

    def _execute_hourly_backup(self):
        filename = self._make_hourly_filename()
        self._backup_database_with_filename(filename)

    def _execute_daily_backup(self):
        filename = self._make_daily_filename()
        self._backup_database_with_filename(filename)

    def _backup_database_with_filename(self, filename):
        _logger.info("Saving the database to minio as filename {}".format(filename))
        with tempfile.NamedTemporaryFile() as file:
            dump_db(self._database_name, file, "dump")
            self._transfer_file_to_minio(filename, file)

    def _transfer_file_to_minio(self, filename, file):
        client = get_minio_client()
        bucket_name = get_backups_bucket_name()
        client.fput_object(bucket_name, filename, file.name)

    def _make_hourly_filename(self):
        return "{db_name}-hourly-{backup_number}.dump".format(
            db_name=self._get_db_name(),
            backup_number=self._get_hourly_backup_number(),
        )

    def _make_daily_filename(self):
        return "{db_name}-daily-{backup_number}.dump".format(
            db_name=self._get_db_name(),
            backup_number=self._get_daily_backup_number(),
        )

    def _get_db_name(self):
        return self.env.cr.dbname

    def _get_hourly_backup_number(self):
        return datetime.now().hour % 3

    def _get_daily_backup_number(self):
        return datetime.now().isoweekday()

    @property
    def _database_name(self):
        return self.env.cr.dbname
