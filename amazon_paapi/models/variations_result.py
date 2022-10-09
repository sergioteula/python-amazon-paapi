from typing import List

from ..sdk import models as sdk_models
from .item_result import Item


class ApiPrice:
    amount: float
    currency: str
    display_amount: str


class ApiVariationDimension:
    display_name: str
    name: str
    values: List[str]


class ApiVariationPrice:
    highest_price: ApiPrice
    lowest_price: ApiPrice


class ApiVariationSummary(sdk_models.VariationSummary):
    page_count: int
    price: ApiVariationPrice
    variation_count: int
    variation_dimensions: List[ApiVariationDimension]


class VariationsResult(sdk_models.VariationsResult):
    items: List[Item]
    variation_summary: ApiVariationSummary
