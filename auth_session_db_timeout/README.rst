Auth Session DB Timeout
=======================
This module acts as a bridge between the `auth_session_timeout` and `session_db` modules from OCA.


Context
-------
By default, Odoo stores sessions in the filestore. The `auth_session_timeout` module follows this logic
and terminates sessions based on a configured timeout.

The `session_db` module enhances performance by storing sessions in the database instead of the filestore.
However, `auth_session_timeout` is not compatible with `session_db` out of the box.

Overview
--------
This module ensures that `auth_session_timeout` works with `session_db` by patching a function in `auth_session_timeout`.
Instead of retrieving session data from the filestore, the module allows sessions to be fetched from
the `http_sessions` table in the database.

- https://github.com/OCA/server-tools/tree/14.0/session_db
- https://github.com/OCA/server-auth/tree/14.0/auth_session_timeout

Contributors
------------

The `Numigi <https://numigi.com/r/home>`_ team is the contributor to this project. We help Quebec companies implement Odoo and Konvergo ERP.
