# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
import subprocess
from odoo.tools.misc import exec_pg_environ
from odoo.addons.numikube_database_backup.bucket import get_backups_bucket_name
from odoo.sql_db import connection_info_for

_logger = logging.getLogger(__name__)


def restore_database(db_name):
    bucket = get_backups_bucket_name()
    db_host = _get_db_host(db_name)
    command = [
        "godoo",
        "restore",
        "--db-host",
        db_host,
        "--bucket",
        bucket,
        "--database",
        db_name,
    ]
    _run_command(command)


def drop_database(db_name):
    db_host = _get_db_host(db_name)
    command = [
        "godoo",
        "dropdb",
        "--db-host",
        db_host,
        "--database",
        db_name,
    ]
    _run_command(command)


def isolate_database(db_name):
    db_host = _get_db_host(db_name)
    command = [
        "godoo",
        "isolate",
        "--db-host",
        db_host,
        "--database",
        db_name,
    ]
    _run_command(command)


def _run_command(command):
    env = exec_pg_environ()
    _logger.info(f"Running command: {command}")
    process = subprocess.run(
        command,
        env=env,
    )
    process.check_returncode()


def _get_db_host(db_name):
    return connection_info_for(db_name)[1]["host"]
