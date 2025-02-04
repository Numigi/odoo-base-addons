Auditlog Binding Queue Job
==========================

This module provides a technical bridge between two OCA modules: `Auditlog` and `Queue Job`.

Once installed, it ensures that the `Auditlog` module does not create logs for requests where the current request name is equal to `queue_job/runjob`. 

This prevents unnecessary log creation for operations initiated by queue jobs, streamlining log management in your Odoo environment.


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
