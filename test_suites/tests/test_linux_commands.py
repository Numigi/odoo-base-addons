"""Check that the linux command lines exists in the docker that will be pushed
"""
import subprocess

from odoo.tests import common, unittest


class CommandLines(common.TransactionCase):
    """Test suite for command lines."""

    def test_updoo(self):
        """  updoo is required."""
        # no assert here, the subprocess will crash if the command doesn't exist.
        subprocess.call(["updoo", "--version"])

    def test_gitoo(self):
        """ gitoo is required"""
        # no assert here, the subprocess will crash if the command doesn't exist.
        subprocess.call(["gitoo", "--version"])

    def test_run_pytest_sh(self):
        """ run_pytest.sh"""
        # no assert here, the subprocess will crash if the command doesn't exist.
        subprocess.call(["run_pytest.sh", "--version"])

    @unittest.skip("Need to find a way to test run_test.sh.")
    def test_run_test_sh(self):
        """ run_pytest.sh"""
        # no assert here, the subprocess will crash if the command doesn't exist.
        subprocess.call(["run_test.sh", "--version"])
