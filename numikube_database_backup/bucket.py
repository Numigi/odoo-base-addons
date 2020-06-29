
from odoo.tools.config import config
from odoo.exceptions import ValidationError

BUCKET_NAME_PARAM = "backups_minio_bucket"


def get_backups_bucket_name():
    bucket_name = config.get(BUCKET_NAME_PARAM)
    if not bucket_name:
        raise ValidationError(
            "The parameter {} is not defined in the odoo conf. "
            "The system can not determine in which bucket to send the database backups."
            .format(BUCKET_NAME_PARAM)
        )
    return bucket_name
