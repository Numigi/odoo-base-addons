# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import tempfile
import logging
import io
import os
import subprocess
from datetime import datetime
from minio import Minio
from odoo.exceptions import ValidationError
from odoo import models
from odoo.service.db import dump_db
from odoo.tools.misc import exec_pg_environ
from odoo.addons.numikube_minio.minio import get_minio_client, auto_create_bucket
from ..bucket import get_backups_bucket_name, is_backups_disabled

_logger = logging.getLogger(__name__)


class DatabaseBackup(models.AbstractModel):

    _name = "numikube.database.backup"
    _description = "Numikube Database Backup"

    def run_backup(self):
        """Run a backup.

        .. deprecated:: 1.1.0

        Method kept for backward compatibility.
        """
        self.run_hourly_backup()

    def run_hourly_backup(self):
        self._check_backups_enabled()
        self._autocreate_backups_bucket()
        self._execute_hourly_backup()

    def run_daily_backup(self):
        self._check_backups_enabled()
        self._autocreate_backups_bucket()
        self._execute_daily_backup()

    def _check_backups_enabled(self):
        if is_backups_disabled():
            raise ValidationError(
                "Database backups are disabled on this Odoo instance."
            )

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
        with tempfile.NamedTemporaryFile(mode="w+b") as file:
            self._dump_db(file.name)
            self._upload_file_with_s3cli(filename, file.name)

    def _dump_db(self, file_path):
        env = exec_pg_environ()
        command = [
            "pg_dump",
            "--format=c",
            "--no-owner",
            "--file={}".format(file_path),
            self._database_name,
        ]
        complete_process = subprocess.run(command, env=env)
        complete_process.check_returncode()

    def _upload_file_with_s3cli(self, filename, file_path):
        bucket = get_backups_bucket_name()
        command = [
            "aws",
            "--endpoint-url",
            "http://minio:9000",
            "s3",
            "cp",
            file_path,
            "s3://{}/{}".format(bucket, filename),
        ]
        env = {
            "AWS_ACCESS_KEY_ID": "minio",
            "AWS_SECRET_ACCESS_KEY": "miniosecret",
            "PATH": os.environ.get("PATH"),
        }
        complete_process = subprocess.run(command, env=env)
        complete_process.check_returncode()

    def _make_hourly_filename(self):
        return "{db_name}-hourly-{backup_number}.dump".format(
            db_name=self._get_db_name(), backup_number=self._get_hourly_backup_number(),
        )

    def _make_daily_filename(self):
        return "{db_name}-daily-{backup_number}.dump".format(
            db_name=self._get_db_name(), backup_number=self._get_daily_backup_number(),
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
