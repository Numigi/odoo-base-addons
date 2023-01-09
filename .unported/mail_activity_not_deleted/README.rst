Mail Activity Not Deleted
=========================
Since version 11.0, Odoo adds the concept of activities.
One issue with this feature is that when an activity is completed, the activity record is deleted from the database.

This module deactivates terminated activities instead of deleting them from the mail_activity table.

New State
---------
The state Done is added to activities. Any completed activity is automatically set to Done.

New Field
---------
The field Date Done is added to activities. When completing the activity, this field is filled with the current time.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
