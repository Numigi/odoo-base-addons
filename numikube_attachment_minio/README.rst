NumiKube Attachment Minio
=========================
This module configures attachments for the Numigi Kubernetes infrastructure.

The module `attachment_minio <https://github.com/hibou-io/hibou-odoo-suite/tree/12.0/attachment_minio>`_
is used for reading and writing attachments from Odoo to a Minio instance.

System Parameters
-----------------
The following ir.parameter values are forced when installing this module.

ir_attachment.location = s3
ir_attachment.location.host = minio:9000
ir_attachment.location.access_key = minio
ir_attachment.location.secret_key = minio_secret
ir_attachment.location.bucket = attachments
ir_attachment.location.secure = False

The attachments are always saved in a minio host at the address minio:9000
inside the same Kubernetes namespace as the current Odoo instance.

The access key and secret are dummy values and the connection is not encrypted.
However, the minio instance is not accessible from the internet.
It is only accessible from inside the Kubernetes cluster.

Post Install
------------
After installing this module, all existing attachments are forced-moved to minio.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)

More information
----------------
* Meet us at https://bit.ly/numigi-com
