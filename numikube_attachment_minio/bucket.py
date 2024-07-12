# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tools.config import config
from odoo.exceptions import ValidationError

BUCKET_NAME_PARAM = "attachment_minio_bucket"


def get_backups_bucket_name():
    bucket_name = config.get(BUCKET_NAME_PARAM)
    if not bucket_name:
        raise ValidationError(
            "The parameter {} is not defined in the odoo conf. "
            "The system can not determine in which bucket to send the attachments."
            .format(BUCKET_NAME_PARAM)
        )
    return bucket_name
