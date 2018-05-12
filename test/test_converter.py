import os.path
import unittest

from io import BytesIO
from unittest import TestCase

from PIL import Image

from converter import Converter, UnsupportedFormat


class TestConverter(TestCase):

    def setUp(self):
        path = os.path.dirname(__file__)

        with open(os.path.join(path, "image.jpg"), "rb") as f:
            self.jpeg_img = f.read()

        with open(os.path.join(path, "image.png"), "rb") as f:
            self.png_img = f.read()

        self.bad_img = b'BaDImaGe'

    def test_same_format(self):
        cvtr = Converter(BytesIO(self.jpeg_img))
        converted = cvtr.to_format("JPEG").read()
        self.assertEqual(self.jpeg_img, converted)

    def test_jpeg_to_png(self):
        cvtr = Converter(BytesIO(self.jpeg_img))
        png = cvtr.to_format("PNG")
        img = Image.open(png)
        self.assertEqual(img.format, "PNG")

    def test_png_to_jpg(self):
        cvtr = Converter(BytesIO(self.png_img))
        png = cvtr.to_format("JPEG")
        img = Image.open(png)
        self.assertEqual(img.format, "JPEG")

    def test_bad_image(self):
        self.assertRaises(UnsupportedFormat, Converter, BytesIO(self.bad_img))

    def test_unsupported_format(self):
        cvtr = Converter(BytesIO(self.jpeg_img))
        self.assertRaises(UnsupportedFormat, cvtr.to_format, "uUnKnowNNn")


if __name__ == '__main__':
    unittest.main()
