from chalice import app


http_errors = {e.STATUS_CODE: e for e in app.ALL_ERRORS}


def raise_by_status_code(code, message):
    klass = http_errors.get(code) or app.ChaliceViewError
    raise klass(message)


def raise_by_boto3_exception(e):
    code = int(e.response['Error']['HTTPStatusCode'])
    msg = e.response['Error']['Message']
    raise_by_status_code(code, msg)
