# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID
from odoo.api import Environment
from odoo.addons.numikube_minio.minio import get_minio_client

BUCKET_NAME = "attachments"


def post_init_hook(cr, _):
    _auto_create_minio_bucket()


def _auto_create_minio_bucket():
    client = get_minio_client()
    bucket_names = {b.name for b in client.list_buckets()}
    if BUCKET_NAME not in bucket_names:
        client.make_bucket(BUCKET_NAME, location="us-east-1")
