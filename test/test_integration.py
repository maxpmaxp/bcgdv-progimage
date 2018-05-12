import json, os.path, unittest

from io import BytesIO
from unittest import TestCase

from chalice.config import Config
from chalice.local import LocalGateway
from PIL import Image
from utils import s3_remove

import app


class TestApp(TestCase):

    def setUp(self):
        path = os.path.dirname(__file__)

        with open(os.path.join(path, "image.jpg"), "rb") as f:
            self.jpeg_img = f.read()

        with open(os.path.join(path, "image.png"), "rb") as f:
            self.png_img = f.read()

        self.lg = LocalGateway(app.app, Config())

        self.tmp_keys = []

    def handle_key(self, tmp_id):
        self.tmp_keys.append(tmp_id)

    def tearDown(self):
        if self.tmp_keys:
            s3_remove(*self.tmp_keys)

    def test_convert_jpeg_to_png(self):
        # POST image
        response = self.lg.handle_request(method='POST',
                                          path='/storage',
                                          headers={'Content-Type': 'image/jpeg'},
                                          body=self.jpeg_img)

        data = json.loads(response['body'])
        self.handle_key(data['id'])

        # Get as PNG
        response = self.lg.handle_request(method='GET',
                                          path='/format/{}.png'.format(data['id']),
                                          headers={}, body='')
        self.assertEqual(response['statusCode'], 200)
        self.assertTrue(response['body'])
        self.assertEqual(Image.open(BytesIO(response['body'])).format, "PNG")

    def test_convert_png_to_jpeg(self):
        # POST image
        response = self.lg.handle_request(method='POST',
                                          path='/storage',
                                          headers={'Content-Type': 'image/png'},
                                          body=self.png_img)
        data = json.loads(response['body'])
        self.handle_key(data['id'])

        # Get as JPG
        response = self.lg.handle_request(method='GET',
                                          path='/format/{}.jpeg'.format(data['id']),
                                          headers={}, body='')
        self.assertEqual(response['statusCode'], 200)
        self.assertTrue(response['body'])
        self.assertEqual(Image.open(BytesIO(response['body'])).format, "JPEG")

    def test_save_get_image(self):
        # POST image
        response = self.lg.handle_request(method='POST',
                                          path='/storage',
                                          headers={'Content-Type': 'image/jpeg'},
                                          body=self.jpeg_img)

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['headers']['Content-Type'], 'application/json')
        data = json.loads(response['body'])
        self.assertTrue(isinstance(data, dict))
        self.assertTrue(data.get('id'))
        self.handle_key(data['id'])
        self.assertEqual(len(data), 1)

        # GET the same image
        response = self.lg.handle_request(method='GET',
                                          path='/storage/{}'.format(data['id']),
                                          headers={},
                                          body='')
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], self.jpeg_img)

    def test_wrong_get_id(self):
        response = self.lg.handle_request(method='GET',
                                          path='/storage/NotExisTinGgggIIid',
                                          headers={}, body='')

        self.assertEqual(response['statusCode'], 404)

    def test_wrong_convert_id(self):
        response = self.lg.handle_request(method='GET',
                                          path='/format/NotExisTinGgggIIid',
                                          headers={}, body='')

        self.assertEqual(response['statusCode'], 404)

        response = self.lg.handle_request(method='GET',
                                          path='/format/NotExisTinGgggIIid.png',
                                          headers={}, body='')

        self.assertEqual(response['statusCode'], 404)

    def test_wrong_convert_format(self):
        # POST image
        response = self.lg.handle_request(method='POST',
                                          path='/storage',
                                          headers={'Content-Type': 'image/jpeg'},
                                          body=self.jpeg_img)
        data = json.loads(response['body'])
        self.handle_key(data['id'])

        # GET image using wrong extension
        response = self.lg.handle_request(method='GET',
                                          path='/format/{data[id]}.BaDForMatT'.format(data=data),
                                          headers={},
                                          body='')
        self.assertEqual(response['statusCode'], 404)

    def test_convert_same_format(self):
        # POST image
        response = self.lg.handle_request(method='POST',
                                          path='/storage',
                                          headers={'Content-Type': 'image/jpeg'},
                                          body=self.jpeg_img)
        data = json.loads(response['body'])
        self.handle_key(data['id'])

        # GET image using .jpeg extension
        response = self.lg.handle_request(method='GET',
                                          path='/format/{data[id]}.jpeg'.format(data=data),
                                          headers={},
                                          body='')
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], self.jpeg_img)

    def test_convert_no_extension(self):
        # POST image
        response = self.lg.handle_request(method='POST',
                                          path='/storage',
                                          headers={'Content-Type': 'image/jpeg'},
                                          body=self.jpeg_img)
        data = json.loads(response['body'])
        self.handle_key(data['id'])

        # GET image using .jpeg extension
        response = self.lg.handle_request(method='GET',
                                          path='/format/{data[id]}'.format(data=data),
                                          headers={},
                                          body='')
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], self.jpeg_img)


if __name__ == '__main__':
    unittest.main()