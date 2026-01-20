# coding: utf-8

"""
Copyright 2025 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

    http://www.apache.org/licenses/LICENSE-2.0

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

"""  # noqa: E501



from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class GetVariationsResource(str, Enum):
    """
    GetVariationsResource
    """

    """
    allowed enum values
    """
    BROWSE_NODE_INFO_DOT_BROWSE_NODES = 'browseNodeInfo.browseNodes'
    BROWSE_NODE_INFO_DOT_BROWSE_NODES_DOT_ANCESTOR = 'browseNodeInfo.browseNodes.ancestor'
    BROWSE_NODE_INFO_DOT_BROWSE_NODES_DOT_SALES_RANK = 'browseNodeInfo.browseNodes.salesRank'
    BROWSE_NODE_INFO_DOT_WEBSITE_SALES_RANK = 'browseNodeInfo.websiteSalesRank'
    CUSTOMER_REVIEWS_DOT_COUNT = 'customerReviews.count'
    CUSTOMER_REVIEWS_DOT_STAR_RATING = 'customerReviews.starRating'
    IMAGES_DOT_PRIMARY_DOT_SMALL = 'images.primary.small'
    IMAGES_DOT_PRIMARY_DOT_MEDIUM = 'images.primary.medium'
    IMAGES_DOT_PRIMARY_DOT_LARGE = 'images.primary.large'
    IMAGES_DOT_PRIMARY_DOT_HIGH_RES = 'images.primary.highRes'
    IMAGES_DOT_VARIANTS_DOT_SMALL = 'images.variants.small'
    IMAGES_DOT_VARIANTS_DOT_MEDIUM = 'images.variants.medium'
    IMAGES_DOT_VARIANTS_DOT_LARGE = 'images.variants.large'
    IMAGES_DOT_VARIANTS_DOT_HIGH_RES = 'images.variants.highRes'
    ITEM_INFO_DOT_BY_LINE_INFO = 'itemInfo.byLineInfo'
    ITEM_INFO_DOT_CONTENT_INFO = 'itemInfo.contentInfo'
    ITEM_INFO_DOT_CONTENT_RATING = 'itemInfo.contentRating'
    ITEM_INFO_DOT_CLASSIFICATIONS = 'itemInfo.classifications'
    ITEM_INFO_DOT_EXTERNAL_IDS = 'itemInfo.externalIds'
    ITEM_INFO_DOT_FEATURES = 'itemInfo.features'
    ITEM_INFO_DOT_MANUFACTURE_INFO = 'itemInfo.manufactureInfo'
    ITEM_INFO_DOT_PRODUCT_INFO = 'itemInfo.productInfo'
    ITEM_INFO_DOT_TECHNICAL_INFO = 'itemInfo.technicalInfo'
    ITEM_INFO_DOT_TITLE = 'itemInfo.title'
    ITEM_INFO_DOT_TRADE_IN_INFO = 'itemInfo.tradeInInfo'
    PARENTASIN = 'parentASIN'
    OFFERS_V2_DOT_LISTINGS_DOT_AVAILABILITY = 'offersV2.listings.availability'
    OFFERS_V2_DOT_LISTINGS_DOT_CONDITION = 'offersV2.listings.condition'
    OFFERS_V2_DOT_LISTINGS_DOT_DEAL_DETAILS = 'offersV2.listings.dealDetails'
    OFFERS_V2_DOT_LISTINGS_DOT_IS_BUY_BOX_WINNER = 'offersV2.listings.isBuyBoxWinner'
    OFFERS_V2_DOT_LISTINGS_DOT_LOYALTY_POINTS = 'offersV2.listings.loyaltyPoints'
    OFFERS_V2_DOT_LISTINGS_DOT_MERCHANT_INFO = 'offersV2.listings.merchantInfo'
    OFFERS_V2_DOT_LISTINGS_DOT_PRICE = 'offersV2.listings.price'
    OFFERS_V2_DOT_LISTINGS_DOT_TYPE = 'offersV2.listings.type'
    VARIATION_SUMMARY_DOT_PRICE_DOT_HIGHEST_PRICE = 'variationSummary.price.highestPrice'
    VARIATION_SUMMARY_DOT_PRICE_DOT_LOWEST_PRICE = 'variationSummary.price.lowestPrice'
    VARIATION_SUMMARY_DOT_VARIATION_DIMENSION = 'variationSummary.variationDimension'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of GetVariationsResource from a JSON string"""
        return cls(json.loads(json_str))



