# Copyright 2024-today Numigi and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tools.config import config
from odoo.exceptions import ValidationError

BUCKET_NAME_PARAM = "backups_minio_bucket"
BACKUPS_DISABLED_PARAM = "backups_disabled"


def get_backups_bucket_name():
    bucket_name = config.get(BUCKET_NAME_PARAM)
    if not bucket_name:
        raise ValidationError(
            "The parameter {} is not defined in the odoo conf. "
            "The system can not determine in which bucket to send the database backups."
            .format(BUCKET_NAME_PARAM)
        )
    return bucket_name


def is_backups_disabled():
    return bool(config.get(BACKUPS_DISABLED_PARAM))
