Queue Job Auto Requeue
======================
This module automatically reset queue jobs to pending after a given time.

Context
-------
One known issue of the module `queue_job <https://github.com/OCA/queue/tree/12.0/queue_job>`_
is that when Odoo crashes or is force-stopped, running jobs remain in ``started`` or ``enqueued`` state.

These jobs not only remain in this state until manually requeued, but they also block other
jobs in the channel from running.

Overview
--------
This module adds a cron that runs every 5 minutes by default.

.. image:: static/description/cron.png

It searches for jobs in ``started`` or ``enqueued`` state.
For each job, it checks if the job has been started more than 5 minutes ago.
If so, the job is requeued.

Custom Time Limit
-----------------
The max time a job can run is parameterizable with the system parameter ``queue_job_time_limit``.
This parameter accepts a value in seconds (i.e. ``600`` for 10 minutes).

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
