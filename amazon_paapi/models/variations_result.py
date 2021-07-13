from .item_result import Item
from ..sdk.models import VariationsResult, VariationSummary

class ApiPrice:
    amount: float
    currency: str
    display_amount: str


class ApiVariationDimension:
    display_name: str
    name: str
    values: list[str]


class ApiVariationPrice:
    highest_price: ApiPrice
    lowest_price: ApiPrice

class ApiVariationSummary(VariationSummary):
    page_count: int
    price: ApiVariationPrice
    variation_count: int
    variation_dimensions: list[ApiVariationDimension]


class VariationsResult(VariationsResult):
    items: list[Item]
    variation_summary: ApiVariationSummary
