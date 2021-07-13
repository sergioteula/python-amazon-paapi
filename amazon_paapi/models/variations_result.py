from typing import List
from .item_result import Item
from ..sdk.models import VariationsResult, VariationSummary

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

class ApiVariationSummary(VariationSummary):
    page_count: int
    price: ApiVariationPrice
    variation_count: int
    variation_dimensions: List[ApiVariationDimension]


class VariationsResult(VariationsResult):
    items: List[Item]
    variation_summary: ApiVariationSummary
