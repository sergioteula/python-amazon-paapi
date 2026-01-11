"""Tests for OffersV2 functionality."""

import unittest

from amazon_paapi.helpers import requests
from amazon_paapi.models.item_result import (
    ApiDealDetails,
    ApiListingsV2,
    ApiOfferPriceV2,
    ApiOfferSavingBasis,
    Item,
)
from amazon_paapi.sdk.models.get_items_resource import GetItemsResource
from amazon_paapi.sdk.models.get_variations_resource import GetVariationsResource
from amazon_paapi.sdk.models.search_items_resource import SearchItemsResource

EXPECTED_OFFERSV2_RESOURCES = [
    "OffersV2.Listings.Availability",
    "OffersV2.Listings.Condition",
    "OffersV2.Listings.DealDetails",
    "OffersV2.Listings.IsBuyBoxWinner",
    "OffersV2.Listings.LoyaltyPoints",
    "OffersV2.Listings.MerchantInfo",
    "OffersV2.Listings.Price",
    "OffersV2.Listings.Type",
]


class TestOffersV2Resources(unittest.TestCase):
    """Test cases for OffersV2 resource constants."""

    def test_get_items_resources_include_all_offersv2(self) -> None:
        """Verify _get_request_resources includes all OffersV2 resources."""
        resources = requests._get_request_resources(GetItemsResource)
        for resource in EXPECTED_OFFERSV2_RESOURCES:
            self.assertIn(resource, resources)

    def test_search_items_resources_include_all_offersv2(self) -> None:
        """Verify _get_request_resources includes all OffersV2 resources for search."""
        resources = requests._get_request_resources(SearchItemsResource)
        for resource in EXPECTED_OFFERSV2_RESOURCES:
            self.assertIn(resource, resources)

    def test_get_variations_resources_include_all_offersv2(self) -> None:
        """Verify _get_request_resources includes OffersV2 resources."""
        resources = requests._get_request_resources(GetVariationsResource)
        for resource in EXPECTED_OFFERSV2_RESOURCES:
            self.assertIn(resource, resources)


class TestOffersV2Models(unittest.TestCase):
    """Test cases for OffersV2 model structure."""

    def test_item_has_offers_v2_attribute(self) -> None:
        """Verify Item class has offers_v2 typed as ApiOffersV2."""
        self.assertIn("offers_v2", Item.__annotations__)
        self.assertEqual(Item.__annotations__["offers_v2"], "ApiOffersV2")

    def test_api_listings_v2_has_required_attributes(self) -> None:
        """Verify ApiListingsV2 has violates_map and deal_details."""
        annotations = ApiListingsV2.__annotations__
        self.assertIn("violates_map", annotations)
        self.assertIn("deal_details", annotations)

    def test_api_deal_details_has_required_attributes(self) -> None:
        """Verify ApiDealDetails has badge and access_type."""
        annotations = ApiDealDetails.__annotations__
        self.assertIn("badge", annotations)
        self.assertIn("access_type", annotations)

    def test_api_offer_price_v2_has_required_attributes(self) -> None:
        """Verify ApiOfferPriceV2 has money and savings."""
        annotations = ApiOfferPriceV2.__annotations__
        self.assertIn("money", annotations)
        self.assertIn("savings", annotations)

    def test_api_offer_saving_basis_has_saving_basis_type(self) -> None:
        """Verify ApiOfferSavingBasis has saving_basis_type."""
        self.assertIn("saving_basis_type", ApiOfferSavingBasis.__annotations__)
