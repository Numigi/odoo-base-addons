Base Selection Label
====================
This module allows to display the value of a selection field of any record.

.. contents:: Table of Contents

Context
-------
In vanilla Odoo, fields of type ``Selection`` are stored as technical strings.

These technical strings are dynamically formatted and translated in the web interface.

However, when you need to display these fields in reports (other than qweb),
it gets complicated.

Overview
--------
After installing this module, a new method ``get_selection_label`` is added on all models.

The method takes in parameter the technical name of the field to display.

.. code-block:: python

    partner = env.ref("base.main_partner")
    label = partner.get_selection_label("lang")
    print(label)

The above code should print the formatted name of the language of the main partner.

Contributors
------------

The `Numigi <https://numigi.com/r/home>`_ team is the contributor to this project. We help Quebec companies implement Odoo and Konvergo ERP.
