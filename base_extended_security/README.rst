Base Extended Security
======================
Allow to define extra security for accessing records through web requests.

.. contents:: Table of Contents

Context
-------
Access rules in Odoo are light.

For example, users with basic rights can view the whole general ledger.
The user only needs to know the correct URL to the list view.

Adding extra access rules to standard Odoo models (res.partner, account.move, stock.move, etc) is risky.
You may end up with unexpected side effects.
Users with basic access will likely encounter error messages when saving records or clicking on action buttons. 

Summary
-------
This module adds access rules that are evaluated at the rpc controller level (instead of the orm level).

Architecture Overview
---------------------
The following methods are added to all models:

* get_extended_security_domain
* check_extended_security_all
* check_extended_security_read
* check_extended_security_write
* check_extended_security_create
* check_extended_security_unlink

These methods act as hooks for injecting search domains and access rights.
By inheriting one of these methods, a module can define custom security rules for a given model.

The module extends the following http routes:

* /web/dataset/call
* /web/dataset/call_kw
* /web/dataset/search_read

The hooks are injected to these routes by the module.

Writing Custom Security Modules
-------------------------------
Suppose that in a specific module, we implement security rules for invoices.

In our scenario, only members of the group ``Purchase / User`` are allowed to access vendor bills.

.. code-block:: python

    from odoo import models, _
    from odoo.exceptions import AccessError
    from odoo.osv.expression import AND


    class Invoice(models.Model):

        _inherit = 'account.invoice'

        def get_extended_security_domain(self):
            result = super().get_extended_security_domain()

            if not self.env.user.has_group('purchase.group_purchase_user'):
                result = AND(result, [('type', 'not in', ('in_invoice', 'in_refunc'))])

            return result

        def check_extended_security_all(self):
            super().get_extended_security_domain()

            supplier_bills = self.filtered(lambda i: i.type in ('in_invoice', 'in_refunc'))

            if supplier_bills and not self.env.user.has_group('purchase.group_purchase_user'):
                raise AccessError(_('You are not allowed to access vendor bills.'))


In this example, if the user is not member of ``Purchase / User``, the invoices of type ``Vendor Bill`` or ``Vendor Refund`` will be masked.

If the user attempts to access the record in read/write/create/delete mode, he will be blocked as well.

However, the module does not presume that the user is allowed or not to access customer invoices.
This is where the approach of this module makes the code easier to reason about than
the native access rules (ir.rule).

Known Limitations
-----------------
This module does not allow do define access rules through the web interface.
The access rules must be coded in modules.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
