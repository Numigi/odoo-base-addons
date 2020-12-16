Prod2x
======

.. contents:: Table of Contents

Context
-------
Since the beginning of Numigi, we have been maintaining a common python library ``updoo`` used
for converting production databases into staging databases.

The source code can be found here:

https://github.com/Numigi/updoo

As extra features need to be isolated, the library becomes bigger and bigger.
Some times, these features are specific to a project. Sometimes, they require a given module to be installed.

Summary
-------
This is a technical module allowing to run custom scripts in order to isolate a production database.

Alone, this module does nothing.

It only adds a model ``prod2x`` and relies on other modules to add behavior to this model.

Usage
-----
When isolating a database, here is how to execute the custom scripts:

.. code-block:: python

    env["prod2x"].run()

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
