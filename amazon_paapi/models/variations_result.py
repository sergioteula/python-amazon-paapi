"""Variations result models for Amazon Product Advertising API."""

from typing import List

from amazon_paapi.sdk import models as sdk_models

from .item_result import Item


class ApiPrice:
    """Represent a price with amount and currency."""

    amount: float
    currency: str
    display_amount: str


class ApiVariationDimension:
    """Represent a variation dimension like size or color."""

    display_name: str
    name: str
    values: List[str]


class ApiVariationPrice:
    """Represent the price range for variations."""

    highest_price: ApiPrice
    lowest_price: ApiPrice


class ApiVariationSummary(sdk_models.VariationSummary):
    """Represent a summary of variations for a product."""

    page_count: int
    price: ApiVariationPrice
    variation_count: int
    variation_dimensions: List[ApiVariationDimension]


class VariationsResult(sdk_models.VariationsResult):
    """Represent the result of a get variations operation."""

    items: List[Item]
    variation_summary: ApiVariationSummary
