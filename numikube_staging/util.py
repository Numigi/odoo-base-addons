# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import requests
import traceback
from datetime import datetime
from functools import wraps
from pytz import timezone
from odoo.tools.config import config


def get_current_timestamp():
    return datetime.now(tz=timezone("Canada/Eastern")).strftime("%Y%m%d_%H%M")


def get_token():
    return config.get("numikube_staging_token")


def with_callback(func):
    @wraps(func)
    def wrapper(callback_url, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as err:
            traceback.print_exc()
            trace = traceback.format_exc()
            _exec_callback_error(callback_url, err, trace)
            raise
        else:
            _exec_callback_done(callback_url)

    return wrapper


def _exec_callback_done(url):
    _exec_callback(url, {"state": "done", "token": get_token()})


def _exec_callback_error(url, error, trace):
    _exec_callback(
        url,
        {
            "state": "error",
            "error": str(error),
            "stacktrace": trace,
            "token": get_token(),
        },
    )


def _exec_callback(url, data):
    try:
        requests.post(url, json=data)
    except Exception:
        traceback.print_exc()
        raise
