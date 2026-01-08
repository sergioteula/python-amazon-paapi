"""Variations result models for Amazon Product Advertising API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from amazon_paapi.sdk import models as sdk_models

if TYPE_CHECKING:
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
    values: list[str]


class ApiVariationPrice:
    """Represent the price range for variations."""

    highest_price: ApiPrice
    lowest_price: ApiPrice


class ApiVariationSummary(sdk_models.VariationSummary):
    """Represent a summary of variations for a product."""

    page_count: int
    price: ApiVariationPrice
    variation_count: int
    variation_dimensions: list[ApiVariationDimension]


class VariationsResult(sdk_models.VariationsResult):
    """Represent the result of a get variations operation."""

    items: list[Item]
    variation_summary: ApiVariationSummary
