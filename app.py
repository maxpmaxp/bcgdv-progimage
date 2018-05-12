import os.path
import uuid

import botocore.exceptions

from chalice import Chalice, Response


import config, utils

from convertor import Convertor, UnsupportedFormat
from exceptions import raise_by_boto3_exception, raise_by_status_code

app = Chalice(app_name='progimage')

# ToDo: Users authentication
# ToDo: Individual buckets per user
# Todo: Format synonyms support: jpg/jpeg, gif/gif89 etc.
# Todo: Correct Content-Type headers for output binary data
# ToDo: Smart images cache: by user, image operation, region etc.
# ToDo: Upload conditions: max image size, check image format is supported etc.
# Todo: Data output improvements: process and output big files by chunks to reduce memory load
# Todo: Bulk uploads support
# ToDo: Roles/Access types support


@app.route('/hello')
def index():
    return {'version': config.version}


@app.route('/format/{filename}')
def convert_format(filename):
    image_id, ext = os.path.splitext(filename)
    # cut leading "."
    if ext.startswith("."):
        ext = ext[1:]
    if not ext:
        return get_image(filename)

    ext = ext.upper()
    try:
        in_stream = utils.s3_download(image_id)
    except botocore.exceptions.ClientError as e:
        raise_by_boto3_exception(e)

    try:
        out = Convertor(in_stream).to_format(ext)
    except UnsupportedFormat:
        # technically this means that the resource doesn't exist
        raise_by_status_code(404, "Unsupported format")
    except IOError:
        raise_by_status_code(400, "Format conversion failed")

    return Response(body=out.read(), status_code=200)


@app.route('/storage/{image_id}')
def get_image(image_id):
    try:
        stream = utils.s3_download(image_id)
    except botocore.exceptions.ClientError as e:
        raise_by_boto3_exception(e)
    return Response(body=stream.read(), status_code=200)


@app.route('/storage',
           content_types=config.supported_content_types,
           methods=['PUT', 'POST'])
def save_image():
    key = str(uuid.uuid4())
    try:
        utils.s3_upload(key, app.current_request.raw_body)
    except botocore.exceptions.ClientError as e:
        raise_by_boto3_exception(e)
    return {"id": key}
