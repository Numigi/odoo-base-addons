Admin Light BI View Editor
==========================
This module restricts access to the menu entries of the bi_view_editor module to all users 
except `Admin Light / Base` and `Administration / Configuration` users.

Usage
-----
* As a user in the `Administration / Configuration` or `Admin Light / Base` user group, 
I go to the `Dashboard` application.

I see that I have access to the `Custom Reports` and `Custom Bi Views` menu entries.

.. image:: static/description/custom_bi_views_menu.png

If I do a search in the search bar on the app panel (if the feature is available like on enterprise edition of Odoo),
, I see the menu.


* As a user not part of the `Administration / Configuration` or `Admin Light / Base` user group, 
I go to the `Dashboard` application.

I see that I don't have access to the `Custom Reports` and `Custom Bi Views` menu entries.

.. image:: static/description/dasbhoard_menu.png

Even if I do a search in the search bar on the app panel (if the feature is available like on enterprise edition of Odoo),
, I see the menu.


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
