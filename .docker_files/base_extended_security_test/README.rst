Base Extended Security Test
===========================

.. contents:: Table of Contents

Context
-------
The module ``base_extended_security`` was developed for Odoo v12.0.

The unit tests were based on the fields ``supplier`` and ``customer`` of ``res.partner``.
These were selected for the tests, because they were unlikely to change in later Odoo versions.

In Odoo v14.0, the unexpected happened, both fields were removed from res.partner.

Overview
--------
This module prevents reimplementing the unit tests with different fields,
therefore, maintaining a test fixture similar for multiple versions of Odoo.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
