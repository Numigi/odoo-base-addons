Lang fr_FR Activated
====================
This module loads the language fr_FR on installation.

Context
-------
When installing Odoo, only en_US is loaded by default.

In Canada, it is better to use fr_FR instead of fr_CA, because the latter one is more or less maintained.

Requirement
-----------
Some modules (such as canada_mis_report) require to load fr_FR translations directly in python
instead of a .po file.

The language must therefore be loaded automatically before installing these modules.

Contributors
------------

The `Numigi <https://numigi.com/r/home>`_ team is the contributor to this project. We help Quebec companies implement Odoo and Konvergo ERP.
