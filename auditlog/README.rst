Audit Log
=========
This module allows to log and view ``create``, ``write`` and ``delete`` operations performed on data.

All fields changed during ``create`` and ``write`` operations are logged.
A field log entry contains the value before and after the operation.

Configuration
-------------
In order to log operations on a model, you need to add an audit rule for that model:

* Go to ``Settings / Technical / Audit / Rules``.
* Select your model (i.e. `Contact`).
* Click on the `Subscribe` button.

.. image:: /auditlog/static/description/rule_form.png

Viewing Field Logs
------------------
Only users of the group ``View Audit Logs`` can view the field logs of a record.

.. image:: /auditlog/static/description/user_form.png

To view the logs of a record:

* Go to the form view.

.. image:: /auditlog/static/description/contact_form.png

* Click on ``Action / Field Logs``.

.. image:: /auditlog/static/description/contact_field_logs.png

Contributors
------------
* Sebastien Alix <sebastien.alix@osiell.com>
* Holger Brunn <hbrunn@therp.nl>
* Holden Rehg <holdenrehg@gmail.com>
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
