import unittest

from unittest import TestCase

import app, config


class TestApp(TestCase):

    def test_hello(self):
        self.assertEqual(app.hello(), {'version': config.version})


if __name__ == '__main__':
    unittest.main()
