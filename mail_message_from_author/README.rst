Mail Message From Author
========================

.. contents:: Table of Contents

Context
-------
In vanilla Odoo, when a portal user logs a message through the portal, the email is sent in the name of OdooBot.

.. image:: static/description/portal_message_post.png

.. image:: static/description/email_received_before.png

Summary
-------
The reason of this behavior is that the ``Author`` field is filled with the portal user, but the ``From``
is left to the default value (``OdooBot``).

.. image:: static/description/mail_message_before.png

After installing this module, whenever a message is created with a given ``Author``, the ``From``
will always be propagated from that author (unless the author has no email in Odoo).

.. image:: static/description/mail_message_after.png

Therefore, when receiving the message in your inbox, the name of the author should be displayed.

.. image:: static/description/email_received_after.png

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
