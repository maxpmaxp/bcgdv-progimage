import io

import boto3

import config


def s3_upload(path, stream, metadata=None):
    s3 = boto3.resource('s3',
                        aws_access_key_id=config.aws_key_id,
                        aws_secret_access_key=config.aws_secret_key)
    bucket = s3.Bucket(config.aws_bucket)
    bucket.put_object(Key=path, Body=stream, Metadata=metadata or {})


def s3_download(key):
    """ returns full file path """
    s3 = boto3.resource('s3',
                        aws_access_key_id=config.aws_key_id,
                        aws_secret_access_key=config.aws_secret_key)
    bucket = s3.Bucket(config.aws_bucket)
    stream = io.BytesIO()
    bucket.download_fileobj(key, stream)
    stream.seek(0)
    return stream
