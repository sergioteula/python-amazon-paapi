from __future__ import annotations

import os
from unittest import TestCase, skipUnless

from amazon_paapi.api import AmazonApi


def get_api_credentials() -> tuple[str]:
    api_key = os.environ.get("API_KEY")
    api_secret = os.environ.get("API_SECRET")
    affiliate_tag = os.environ.get("AFFILIATE_TAG")
    country_code = os.environ.get("COUNTRY_CODE")

    return api_key, api_secret, affiliate_tag, country_code


@skipUnless(all(get_api_credentials()), "Needs Amazon API credentials")
class IntegrationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        api_key, api_secret, affiliate_tag, country_code = get_api_credentials()
        cls.api = AmazonApi(api_key, api_secret, affiliate_tag, country_code)
        cls.affiliate_tag = affiliate_tag

    def test_search_items_and_get_information_for_the_first_one(self):
        search_result = self.api.search_items(keywords="zapatillas")
        searched_item = search_result.items[0]

        self.assertEqual(10, len(search_result.items))
        self.assertIn(self.affiliate_tag, searched_item.detail_page_url)

        get_results = self.api.get_items(searched_item.asin)

        self.assertEqual(1, len(get_results))
        self.assertIn(self.affiliate_tag, get_results[0].detail_page_url)
