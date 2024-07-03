# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
from odoo.exceptions import AccessError
from odoo.tests import BaseCase
from odoo.tools.config import config
from ..staging import get_db_name, validate_token
from ..util import get_current_timestamp


class TestStaging(BaseCase):

    def test_db_name(self):
        db_name = get_db_name({
            "level": "lab",
            "client": "isidor",
        })
        assert db_name == "isidor-lab"

    def test_db_name__with_suffix(self):
        db_name = get_db_name({
            "level": "lab",
            "client": "isidor",
            "suffix": "my_suffix",
        })
        assert db_name == "isidor-lab_my_suffix"

    def test_db_name__with_timestamp_and_suffix(self):
        timestamp = get_current_timestamp()
        db_name = get_db_name({
            "level": "lab",
            "client": "isidor",
            "suffix": "my_suffix",
            "timestamp": True,
        })
        assert db_name == f"isidor-lab_{timestamp}_my_suffix"

    def test_validate_token(self):
        token = "xxx"
        config["numikube_staging_token"] = token
        validate_token({"token": token})

    def test_validate_token__wrong_value(self):
        token = "xxx"
        config["numikube_staging_token"] = token
        with pytest.raises(AccessError):
            validate_token({"token": "wrong_value"})

    def test_validate_token__undefined_token(self):
        config["numikube_staging_token"] = None
        with pytest.raises(AccessError):
            validate_token({"token": None})
