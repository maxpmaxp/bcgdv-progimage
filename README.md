========================================
ProgImage - Python Serverless API
========================================

It runs on Amazon API gateway + AWS Lambda + Amazon S3


Based on Chalice micro-framework.
The documentation is available
`on readthedocs <http://chalice.readthedocs.io/en/latest/>`__.


AWS Credentials
---------------

Before you can deploy an application, be sure you have
credentials configured.  If you have previously configured your
machine to run boto3 (the AWS SDK for Python) or the AWS CLI then
you can skip this section.

If this is your first time configuring credentials for AWS you
can follow these steps to quickly get started::

    $ mkdir ~/.aws
    $ cat >> ~/.aws/config
    [default]
    aws_access_key_id=YOUR_ACCESS_KEY_HERE
    aws_secret_access_key=YOUR_SECRET_ACCESS_KEY
    region=YOUR_REGION (such as us-west-2, us-west-1, etc)

If you want more information on all the supported methods for
configuring credentials, see the
`boto3 docs
<http://boto3.readthedocs.io/en/latest/guide/configuration.html>`__.


Then create bucket ``bcgdv.progimage`` and `set role
<http://www.awslessons.com/2017/accessing-s3-with-lambda-functions/>`__.
` for your lambda to access S3


Installation
------------

::

    $ git checkout https://github.com/maxpmaxp/bcgdv-progimage.git
    $ cd bcgdv-progimage
    $ virtualenv -p python3 -q --no-site-packages .venv
    $ .venv/bin/pip install --upgrade -r ./requirements.txt


Deploying
---------

Let's deploy this app.  Make sure you're in the ``bcgdv-progimage``
directory and run ``chalice deploy``::

    $ chalice deploy
    ...
    Updating policy for IAM role: progimage-dev
    Updating lambda function: progimage-dev
    Updating rest API
    Resources deployed:
      - Lambda ARN: arn:aws:lambda:us-west-1:656282194048:function:progimage-dev
      - Rest API URL: https://0ro7r0j70a.execute-api.us-west-1.amazonaws.com/api/

You now have an API up and running using API Gateway and Lambda::

    $ curl https://0ro7r0j70a.execute-api.us-west-1.amazonaws.com/api/hello
    {"version": "0.1"}


Tutorial: API methods
========================

For the rest of these tutorials, we'll be using ``httpie`` instead of ``curl``
(https://github.com/jakubroztocil/httpie) to test our API.  You can install
``httpie`` using ``pip install httpie``, or if you're on Mac, you can run
``brew install httpie``.  The Github link has more information on installation
instructions.  Here's an example of using ``httpie`` to request the root
resource of the API we just created.  Note that the command name is ``http``::


Upload image

    $ cat image.jpeg | http POST https://endpoint/api/storage Content-Type:image/jpeg
    HTTP/1.1 200 OK

    {
        "id": "76b2561b-5619-11e8-a031-c14c98f4a8a1"
    }


Get image

    $ http https://endpoint/api/storage/76b2561b-5619-11e8-a031-c14c98f4a8a1
    HTTP/1.1 200 OK
    Content-Length: 130280
    ...

Convert image format

    $ http https://endpoint/api/format/76b2561b-5619-11e8-a031-c14c98f4a8a1.png
    HTTP/1.1 200 OK
    Content-Length: 138176
    ...

