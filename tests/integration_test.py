import os
from unittest import TestCase, skipUnless


def are_credentials_defined() -> bool:
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    affiliate_tag = os.environ.get("AFFILIATE_TAG")
    country_code = os.environ.get("COUNTRY_CODE")

    return all([api_key, api_secret, affiliate_tag, country_code])


@skipUnless(are_credentials_defined(), "Needs Amazon API credentials")
class IntegrationTest(TestCase):
    def test_it_works(self):
        self.assertTrue(True)
