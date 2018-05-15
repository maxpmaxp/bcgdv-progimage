import io

import boto3

from chalicelib import config

aws_access_key_id="AKIAJ2FLNHDUTS3VAPTA"
aws_secret_access_key="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"


def s3_upload(path, stream, metadata=None):
    s3 = boto3.resource('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
    bucket = s3.Bucket(config.aws_bucket)
    bucket.put_object(Key=path, Body=stream, Metadata=metadata or {},)


def s3_download(key):
    s3 = boto3.resource('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)
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