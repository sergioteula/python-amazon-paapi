import unittest

from amazon_paapi.errors import AmazonError


class TestAmazonError(unittest.TestCase):
    def test_amazon_error_str(self):
        error = AmazonError("Test reason")

        self.assertEqual("Test reason", str(error))
