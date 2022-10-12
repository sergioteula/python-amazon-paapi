from typing import List, Optional

from ..sdk import models as sdk_models


class ApiLabelLocale:
    label: str
    locale: str


class ApiMultiValuedAttributeStr(ApiLabelLocale, sdk_models.MultiValuedAttribute):
    display_values: List[str]


class ApiDisplayValuesType:
    display_value: str
    type: str


class ApiMultiValuedAttributeType(ApiLabelLocale, sdk_models.MultiValuedAttribute):
    display_values: List[ApiDisplayValuesType]


class ApiUnitBasedAttribute(ApiLabelLocale, sdk_models.UnitBasedAttribute):
    display_value: float
    unit: str


class ApiSingleStringValuedAttribute(
    ApiLabelLocale, sdk_models.SingleStringValuedAttribute
):
    display_value: str


class ApiSingleBooleanValuedAttribute(
    ApiLabelLocale, sdk_models.SingleBooleanValuedAttribute
):
    display_value: bool


class ApiSingleIntegerValuedAttribute(
    ApiLabelLocale, sdk_models.SingleIntegerValuedAttribute
):
    display_value: float


class ApiPrice:
    amount: float
    currency: str
    price_per_unit: float
    display_amount: str
    price_type: sdk_models.PriceType
    price_type_label: str


class ApiImageSize(sdk_models.ImageSize):
    url: str
    height: str
    width: str


class ApiImageType(sdk_models.ImageType):
    large: ApiImageSize
    medium: ApiImageSize
    small: ApiImageSize


class ApiImages(sdk_models.Images):
    primary: ApiImageType
    variants: List[ApiImageType]


class ApiByLineInfo(sdk_models.ByLineInfo):
    brand: ApiSingleStringValuedAttribute
    contributors: ApiSingleStringValuedAttribute
    manufacturer: ApiSingleStringValuedAttribute


class ApiClassifications(sdk_models.Classifications):
    binding: ApiSingleStringValuedAttribute
    product_group: ApiSingleStringValuedAttribute


class ApiContentInfo(sdk_models.ContentInfo):
    edition: ApiSingleStringValuedAttribute
    languages: ApiMultiValuedAttributeType
    publication_date: Optional[ApiSingleStringValuedAttribute]


class ApiContentRating(sdk_models.ContentRating):
    audience_rating: ApiSingleStringValuedAttribute


class ApiExternalIds(sdk_models.ExternalIds):
    ea_ns: ApiMultiValuedAttributeStr
    isb_ns: ApiMultiValuedAttributeStr
    up_cs: ApiMultiValuedAttributeStr


class ApiFeatures:
    features: ApiMultiValuedAttributeStr


class ApiManufactureInfo(sdk_models.ManufactureInfo):
    item_part_number: ApiSingleStringValuedAttribute
    model: ApiSingleStringValuedAttribute
    warranty: ApiSingleStringValuedAttribute


class ApiItemDimensions(sdk_models.DimensionBasedAttribute):
    height: ApiUnitBasedAttribute
    length: ApiUnitBasedAttribute
    weight: ApiUnitBasedAttribute
    width: ApiUnitBasedAttribute


class ApiProductInfo(sdk_models.ProductInfo):
    color: ApiSingleStringValuedAttribute
    is_adult_product: ApiSingleBooleanValuedAttribute
    item_dimensions: ApiItemDimensions
    release_date: ApiSingleStringValuedAttribute
    size: ApiSingleStringValuedAttribute
    unit_count: ApiSingleIntegerValuedAttribute


class ApiTechnicalInfo(sdk_models.TechnicalInfo):
    formats: ApiMultiValuedAttributeStr
    energy_efficiency_class: ApiSingleStringValuedAttribute


class ApiTradeInPrice(sdk_models.TradeInPrice):
    amount: float
    currency: str
    display_amount: str


class ApiTradeInInfo(sdk_models.TradeInInfo):
    is_eligible_for_trade_in: bool
    price: ApiTradeInPrice


class ApiItemInfo(sdk_models.ItemInfo):
    by_line_info: ApiByLineInfo
    classifications: ApiClassifications
    content_info: Optional[ApiContentInfo]
    content_rating: ApiContentRating
    external_ids: ApiExternalIds
    features: ApiFeatures
    manufacture_info: ApiManufactureInfo
    product_info: Optional[ApiProductInfo]
    technical_info: ApiTechnicalInfo
    title: ApiSingleStringValuedAttribute
    trade_in_info: ApiTradeInInfo


class ApiOfferAvailability(sdk_models.OfferAvailability):
    max_order_quantity: int
    message: str
    min_order_quantity: int
    type: str


class ApiOfferConditionInfo:
    display_value: str
    label: str
    locale: str
    value: str


class ApiOfferSubCondition(ApiOfferConditionInfo, sdk_models.OfferSubCondition):
    pass


class ApiOfferConditionNote(sdk_models.OfferConditionNote):
    locale: str
    value: str


class ApiOfferCondition(ApiOfferConditionInfo, sdk_models.OfferCondition):
    sub_condition: ApiOfferSubCondition
    condition_note: ApiOfferConditionNote


class ApiOfferDeliveryInfo(sdk_models.OfferDeliveryInfo):
    is_amazon_fulfilled: bool
    is_free_shipping_eligible: bool
    is_prime_eligible: bool


class ApiOfferLoyaltyPoints(sdk_models.OfferLoyaltyPoints):
    points: int


class ApiOfferMerchantInfo(sdk_models.OfferMerchantInfo):
    default_shipping_country: str
    feedback_count: int
    feedback_rating: float
    id: str
    name: str


class ApiOfferSavings(ApiPrice, sdk_models.OfferSavings):
    percentage: float


class ApiOfferPrice(ApiPrice, sdk_models.OfferPrice):
    savings: sdk_models.OfferSavings


class ApiOfferProgramEligibility(sdk_models.OfferProgramEligibility):
    is_prime_exclusive: bool
    is_prime_pantry: bool


class ApiPromotion(ApiPrice, sdk_models.OfferPromotion):
    type: str
    discount_percent: float


class ApiListings(sdk_models.OfferListing):
    availability: ApiOfferAvailability
    condition: ApiOfferCondition
    delivery_info: ApiOfferDeliveryInfo
    id: str
    is_buy_box_winner: bool
    loyalty_points: ApiOfferLoyaltyPoints
    merchant_info: ApiOfferMerchantInfo
    price: ApiOfferPrice
    program_eligibility: ApiOfferProgramEligibility
    promotions: List[ApiPromotion]
    saving_basis: ApiPrice
    violates_map: bool


class ApiOffers(sdk_models.Offers):
    listings: List[ApiListings]


class ApiBrowseNode(sdk_models.BrowseNode):
    ancestor: str
    context_free_name: str
    display_name: str
    id: str
    is_root: str
    sales_rank: str


class ApiWebsiteSalesRank(sdk_models.WebsiteSalesRank):
    context_free_name: str
    display_name: str
    sales_rank: str


class ApiBrowseNodeInfo(sdk_models.BrowseNodeInfo):
    browse_nodes: List[ApiBrowseNode]
    website_sales_rank: ApiWebsiteSalesRank


class Item(sdk_models.Item):
    asin: str
    browse_node_info: ApiBrowseNodeInfo
    customer_reviews: sdk_models.CustomerReviews
    detail_page_url: str
    images: ApiImages
    item_info: ApiItemInfo
    offers: ApiOffers
    parent_asin: str
    rental_offers: sdk_models.RentalOffers
    score: float
    variation_attributes: List[sdk_models.VariationAttribute]
