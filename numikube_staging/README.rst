Numikube Staging
================

.. contents:: Table of Contents

Context
-------
In the first three years of Numigi, starting a prod2lab was a task that could only
be done by an analyst at Numigi.

This would be done using `Alfred <https://alfred.numigi.net>`_.

When a client would want a new lab database, he would create a ticket in isidor.
This is non-efficient and time consuming for both the analyst and the client.

Hypothesis
----------
A solution that was analysed as workaround was to give our clients access to Alfred.

This solution was discarded because of the security issues.
Access management in Jenkins is complicated.

Also, it would mean another system on which to train our clients.

Module Design
-------------
The module creates a bridge between a production and a staging environment.

The staging environment is responsible to create the new database using a set of
parameters given by the production.

The production environment allows the client to trigger the staging job.

Once a job is triggered an HTTP request is sent from the production to the staging environment.
The json data of the request contains a token.
This token must match a token defined in the configuration of the staging.

This HTTP request does not wait until the execution of the staging job.
It returns with the name of the future database.
The actual process of preparing the new database is ran in a thread on the staging environment.

When the job is done, an HTTP request is sent to the production environment using
a callback url.

The job information is updated on the production and an email is sent to the user.

Configuration
-------------

Production
~~~~~~~~~~
The module needs to be installed in production. Two possibilities for this:

1. By default, the numikube_staging module is declared as `server_wide_modules` in the odoo.conf of odoo-base.

See: https://github.com/Numigi/odoo-base/blob/12.0/odoo.conf

2. In some cases where there is a specific odoo.conf, it need to be specified in the odoo_specific.conf of the client so that it is not overwritted.

For example: https://github.com/Numigi/cosmos-odoo/blob/12.0/odoo_specific.conf

Staging
~~~~~~~
The module also needs to be loaded as server-wide module in
the target staging (lab / test) environment.

The staging configuration must also specify:
* the token
* the minio bucket to use for backups (or else it will fallback to dev-backups specified in odoo-base config)

Example of configuration of the staging environment.

.. code-block:: ini

   [options]
   server_wide_modules = web,numikube_staging
   numikube_staging_token = xxx_your_staging_token_xxx
   backups_minio_bucket = isidor-backups

In the production environment, as administrator, I go to ``Administration / Staging / Environments``.

.. image:: numikube_staging/static/description/environment_list.png

I create a new environment called ``Lab``.

.. image:: numikube_staging/static/description/environment_form.png

1. Under ``URL``, I put the URL of the staging instance.

   In the example, ``localhost:8069`` means that the staging is in fact
   the same instance as the production.

2. Under ``Client``, I put the technical name of the client (i.e. cosmos, flex, isidor).

3. Under ``Level``, I select ``Lab``.

4. Under ``Token``, I put the exact same value as defined
   above in the configuration of the staging environment.

Usage
-----
The module adds a new user group ``Admin Light / Run Staging``.

.. image:: numikube_staging/static/description/user_form.png

As member of this new group, I go to ``Administration / Staging / Jobs``.

I find the list of staging jobs.

.. image:: numikube_staging/static/description/job_list.png

I create a new job.

.. image:: numikube_staging/static/description/job_form.png

1. As environment, I select ``Lab``.

2. By default, the box ``Timestamp`` is checked.
   This allows the date and time to appear in the name of the database.

3. In ``Suffix``, I enter a chain of caracters that should appear at the end
   of the database name.

After saving, I click on ``Run``.

.. image:: numikube_staging/static/description/job_form_run.png

After clicking on ``Run``, the state of the job is set to ``Running``.

.. image:: numikube_staging/static/description/job_form_running.png

At this point, the staging database is being built by the staging environment.

The database name is shown because this information is already available,
even though the database is not ready to be used.

A few seconds (or minutes later), I refresh the form view.

I notice that the job is done and that an email was sent to inform me.

.. image:: numikube_staging/static/description/job_form_done.png

Inside the email, a clickable link allows to access the staging environment
and select the database.

.. image:: numikube_staging/static/description/job_form_done_email_link.png

.. image:: numikube_staging/static/description/staging_database_selector.png


Constraints
-----------
The``Suffix`` field should not contain any spaces, special characters, or uppercase letters.

.. image:: numikube_staging/static/description/suffix_constraint.png


Jobs In Error
-------------
In case of an error, the status is set to ``Error``.

A different email is sent to inform the user of the error.

.. image:: numikube_staging/static/description/job_form_error.png

A job in ``Error`` can be retried by clicking again on ``Run``.

Drop Databases
--------------
Since version ``1.2.0`` of the module, it is possible to drop databases using a staging job.

When creating a new job, a new field ``Type`` allows you to choose between:

* ``New Database``
* ``Drop Databases``

.. image:: numikube_staging/static/description/job_form_type.png

After selecting ``Drop Databases``, a new field ``Database Names`` appears.

I enter the list of database names to delete.

.. image:: numikube_staging/static/description/dropdb_database_names.png

..

   The names of the databases can be separated by spaces or line breaks.

A dropdb job is completed synchronously in a few seconds.

It does not run in background like when creating a new database.
The reason is that droping a database is fast.

.. image:: numikube_staging/static/description/dropdb_done.png

Database Limit
--------------
By default, the module limits the number of database in a single instance to ``10`` databases.

It is possible to change this limit for a given instance.
This is done by defining the odoo config parameter ``numikube_staging_database_limit``.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
