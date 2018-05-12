import io

import boto3

from . import config


def s3_upload(path, stream, metadata=None):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(config.aws_bucket)
    bucket.put_object(Key=path, Body=stream, Metadata=metadata or {})


def s3_download(key):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(config.aws_bucket)
    stream = io.BytesIO()
    bucket.download_fileobj(key, stream)
    stream.seek(0)
    return stream


def s3_remove(*keys):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(config.aws_bucket)
    bucket.delete_objects(
        Delete={
            'Objects': [{'Key': k} for k in keys]
        }
    )