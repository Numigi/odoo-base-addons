Auth Session Redis Timeout
==========================
Binding between `Session Redis <https://github.com/camptocamp/odoo-cloud-platform/tree/12.0/session_redis>`_ Module and `Auth Session Timeout <https://github.com/OCA/server-auth/tree/12.0/auth_session_timeout>`_  Module. 
This module is able to kill(logout) all inactive redis sessions since a given delay. 
On each request the server checks if the session is yet valid regarding the expiration delay. 
If not a clean logout is operated.


Configuration
-------------

The two system parameters of the module `Auth Session Timeout` are available:

- inactive_session_time_out_delay: validity of a session in seconds (default = 2 Hours)
- inactive_session_time_out_ignored_url: technical urls where the check does not occur


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
