Ir Attachment Access Token Portal
=================================
This module grant access to documents to the portal user.
Due to security restriction, the portal user would see a error 500 if it tries to 
read a task that have a document.
The error comes from the write required by the update of the access token.

This module sudo the write to allow the portal user to have access to the documents.

See TA#6109


Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
