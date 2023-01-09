Base Extended Security / Grid
=============================
The module ``base_extended_security`` allows to define extra security for accessing records through web requests.

This module makes the extra security features compatible with the module ``web_grid`` (Odoo Enterprise).

.. contents:: Table of Contents

Context
-------
The module ``web_grid`` adds a method ``read_grid`` (callable with XML-rpc).
This method is similar to ``read_group``. It reads data about a record based on a domain.

Module Design
-------------
Instead of injecting new code in the controller layer, this module simply inherits the method ``read_grid``.

The reason is that ``read_grid`` is only called directly through XML-rpc.
In contrast, other standard methods such as ``read_group`` and ``search_read`` are called
intensively from the internal code Odoo.

Inheriting the method ``read_grid`` is unlikely to create side effects as it would be to inherit other base methods.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
