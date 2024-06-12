
import logging
from minio import Minio

_logger = logging.getLogger()


def auto_create_bucket(bucket_name):
    _logger.info("Creating bucket {} if not exists".format(bucket_name))
    available_bucket_names = get_bucket_names()
    if bucket_name in available_bucket_names:
        _logger.info("Bucket {} exists".format(bucket_name))
    else:
        _logger.info("Creating bucket {}".format(bucket_name))
        client = get_minio_client()
        client.make_bucket(bucket_name, location="us-east-1")


def get_bucket_names():
    client = get_minio_client()
    return [b.name for b in client.list_buckets()]


def get_minio_client():
    return Minio(
        "minio:9000",
        access_key="minio",
        secret_key="miniosecret",
        secure=False,
    )
