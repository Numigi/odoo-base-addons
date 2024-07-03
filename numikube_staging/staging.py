# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from threading import Thread
from odoo import _
from odoo.exceptions import AccessError
from odoo.http import db_list
from odoo.tools.config import config
from .godoo import drop_database, restore_database, isolate_database
from .util import get_current_timestamp, get_token, with_callback

_logger = logging.getLogger(__name__)

DEFAULT_DATABASE_LIMIT = 10


def run_staging_job(data):
    validate_token(data)

    _logger.info(data)

    if data["type"] == "prod2x":
        return _run_prod2x_job(data)

    elif data["type"] == "dropdb":
        return _run_dropdb_job(data)


def _run_prod2x_job(data):
    _check_number_databases_limit()
    db_name = get_db_name(data)
    callback_url = get_callback_url(data)
    thread = Thread(target=run_prod2x, args=(callback_url, db_name))
    thread.start()
    return {"db_name": db_name}


@with_callback
def run_prod2x(db_name):
    from updoo.prod2x import prod2x
    drop_database(db_name)
    restore_database(db_name)
    isolate_database(db_name)
    prod2x(db_name)


def get_db_name(data):
    client = data["client"]
    level = data["level"]
    db_name = f"{client}-{level}"

    if data.get("timestamp"):
        timestamp = get_current_timestamp()
        db_name += f"_{timestamp}"

    suffix = data.get("suffix")
    if suffix:
        db_name += f"_{suffix}"

    return db_name


def get_callback_url(data):
    return data["callback"]


def validate_token(data):
    token = data.get("token")
    if not token:
        raise AccessError(_("You must supplied a staging token in the json data."))

    if token != get_token():
        raise AccessError(_("The supplied staging token does not match."))


def _check_number_databases_limit():
    dbs = db_list(force=True)
    limit = _get_database_limit()

    if len(dbs) >= limit:
        raise AccessError(_(
            "The number of databases on this staging exceeds the limit. "
            "You may not have more than {} active databases on this instance."
        ).format(limit))


def _get_database_limit():
    return config.get("numikube_staging_database_limit") or DEFAULT_DATABASE_LIMIT


def _run_dropdb_job(data):
    db_names = data["database_names"]

    db_names_ = (d.strip() for d in db_names.split())
    for db in db_names_:
        _drop_single_database(db)

    return {"status": "done"}


def _drop_single_database(db_name):
    available_dbs = db_list(force=True)

    if db_name in available_dbs:
        drop_database(db_name)
    else:
        _logger.warning(
            f"Could not drop database {db_name}, the database in not present in "
            f"the list of databases of this instance."
        )
