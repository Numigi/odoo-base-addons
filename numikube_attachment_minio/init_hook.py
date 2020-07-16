# © 2020 - today Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import SUPERUSER_ID
from odoo.api import Environment
from odoo.addons.numikube_minio.minio import get_minio_client, auto_create_bucket

BUCKET_NAME = "attachments"


def post_init_hook(cr, _):
    _auto_create_minio_bucket()
    _transfer_existing_attachments_to_minio(cr)


def _transfer_existing_attachments_to_minio(cr):
    with Environment.manage():
        env = Environment(cr, SUPERUSER_ID, {})
        attachments = env["ir.attachment"].search([])
        for attachment in attachments:
            attachment.datas = attachment.datas


def _auto_create_minio_bucket():
    client = get_minio_client()
    bucket_names = {b.name for b in client.list_buckets()}
    if BUCKET_NAME not in bucket_names:
        client.make_bucket(BUCKET_NAME, location="us-east-1")