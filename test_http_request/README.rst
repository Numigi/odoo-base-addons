Test HTTP Request
-----------------
A technical Odoo module to help testing HTTP requests/controllers.

This module does not need to be in the dependencies of other modules that use it.
However, if installed, it will have no impact on a production instance.

Context
-------
Testing HTTP controllers in Odoo is not a trivial task.
Therefore, many developpers do not automate the tests of their controllers. This is a mistake.

This modules intends to offer tools to make the task easier.

Usage
-----

Mocking HTTP Requests
~~~~~~~~~~~~~~~~~~~~~
The first tool this module provides is a way to mock Odoo HTTP requests.

In your module, you may use the ``mock_odoo_request`` to simulate the request:

.. code-block:: python

    from odoo.addons.test_http_request.common import mock_odoo_request
    from odoo.tests.common import TransactionCase
    from ..controllers.main import MyController


    class TestSomething(TransactionCase):

        def test_some_method(self):
            with mock_odoo_request(self.env):
                result = MyController().do_something()

            assert result == ...


The ``mock_odoo_request`` function is a context manager.
Behind the scene, when calling it, the following technical work is done:

* An HTTP session is created.
* An environ is created.
* An httprequest object is added to the werkzeug stack.
* The httprequest object is bound to the given ``Odoo Environment`` object.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
