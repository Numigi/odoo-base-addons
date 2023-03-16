# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import pytest
import requests_mock
from contextlib import contextmanager
from odoo.exceptions import AccessError, ValidationError
from odoo.tests import SavepointCase
from ..callback import run_callback


class TestStaging(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.url = "http://lab.example.com"
        cls.webhook_url = f"{cls.url}/web/staging/run"
        cls.token = "xxxx"
        cls.client = "cosmos"
        cls.level = "lab"
        cls.db_name = "cosmos-lab"

        cls.environment = cls.env["staging.environment"].create(
            {
                "name": "Lab",
                "url": cls.url,
                "token": cls.token,
                "client": cls.client,
                "level": cls.level,
            }
        )

        cls.suffix = "my_suffix"
        cls.job = cls.env["staging.job"].create(
            {
                "environment_id": cls.environment.id,
                "suffix": cls.suffix,
                "timestamp": True,
            }
        )

        cls.base_url = "http://example.com"
        cls.env["ir.config_parameter"].set_param("web.base.url", cls.base_url)

    def test_run(self):
        with self.mock_webhook():
            self.job.run()

        assert self.job.state == "running"
        assert self.job.database_name == self.db_name

    def test_run__with_error(self):
        error = "Some error occured"

        with self.mock_webhook_with_error(error):
            self.job.run()

        assert self.job.state == "error"
        assert self.job.error == error

    def test_run__with_odoo_error(self):
        error = "Some error occured"
        traceback = "Traceback (most recent call last): ..."

        with self.mock_webhook_with_odoo_error(error, traceback):
            self.job.run()

        assert self.job.state == "error"
        assert self.job.error == error
        assert self.job.traceback == traceback

    def test_webhook_data(self):
        data = self.job._get_webhook_data()
        assert data["token"] == self.token
        assert data["level"] == self.level
        assert data["client"] == self.client
        assert data["suffix"] == self.suffix
        assert data["timestamp"] is True
        assert data["callback"] == f"{self.base_url}/web/staging/callback/{self.job.id}"

    def test_webhook_data__base_url_undefined(self):
        self.env["ir.config_parameter"].set_param("web.base.url", "")
        with pytest.raises(ValidationError):
            self.job._get_webhook_data()

    def test_run_callback(self):
        data = {"state": "done", "token": self.token}
        run_callback(self.env, self.job.id, data)
        assert self.job.state == "done"

    def test_run_callback_error(self):
        error = "Some error occured"
        traceback = "Traceback (most recent call last): ..."
        data = {
            "state": "error",
            "error": error,
            "traceback": traceback,
            "token": self.token,
        }
        run_callback(self.env, self.job.id, data)
        assert self.job.state == "error"
        assert self.job.error == error
        assert self.job.traceback == traceback

    def test_run_callback__wrong_token(self):
        data = {"state": "done", "token": "wrong_token"}
        with pytest.raises(AccessError):
            run_callback(self.env, self.job.id, data)

    def test_check_suffix_contains_uppercase(self):
        with pytest.raises(ValidationError):
            self.job.suffix = 'Test'

    def test_check_suffix_contains_special_character(self):
        with pytest.raises(ValidationError):
            self.job.suffix = 'test?'

    def test_check_suffix_contains_space(self):
        with pytest.raises(ValidationError):
            self.job.suffix = 'test0 test1'

    def test_check_suffix_contains_underscore_or_dash(self):
        self.job.suffix = 'test0_test1-test2'
        assert self.job.suffix

    @contextmanager
    def mock_webhook(self):
        data = {"result": {"db_name": self.db_name}}
        with requests_mock.Mocker() as m:
            m.post(self.webhook_url, json=data)
            yield m

    @contextmanager
    def mock_webhook_with_error(self, error):
        with requests_mock.Mocker() as m:
            m.post(self.webhook_url, status_code=500, text=error)
            yield m

    @contextmanager
    def mock_webhook_with_odoo_error(self, error, traceback):
        data = {
            "error": {
                "data": {
                    "message": error,
                    "debug": traceback,
                }
            }
        }
        with requests_mock.Mocker() as m:
            m.post(self.webhook_url, json=data)
            yield m
