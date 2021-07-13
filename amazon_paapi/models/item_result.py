from typing import List
from ..sdk import models

"""Shared models"""
class ApiLabelLocale:
    label: str
    locale: str

class ApiMultiValuedAttributeStr(ApiLabelLocale, models.MultiValuedAttribute):
    display_values: List[str]

class ApiDisplayValuesType:
    display_value: str
    type: str

class ApiMultiValuedAttributeType(ApiLabelLocale, models.MultiValuedAttribute):
    display_values: List[ApiDisplayValuesType]

class ApiUnitBasedAttribute(ApiLabelLocale, models.UnitBasedAttribute):
    display_value: float
    unit: str

class ApiSingleStringValuedAttribute(ApiLabelLocale, models.SingleStringValuedAttribute):
    display_value: str

class ApiSingleBooleanValuedAttribute(ApiLabelLocale, models.SingleBooleanValuedAttribute):
    display_value: bool

class ApiSingleIntegerValuedAttribute(ApiLabelLocale, models.SingleIntegerValuedAttribute):
    display_value: float

class ApiPrice:
    amount: float
    currency: str
    price_per_unit: float
    display_amount: str

"""Image models"""
class ApiImageSize(models.ImageSize):
    url: str
    height: str
    width: str

class ApiImageType(models.ImageType):
    large: ApiImageSize
    medium: ApiImageSize
    small: ApiImageSize

class ApiImages(models.Images):
    primary: ApiImageType
    variants: List[ApiImageType]

"""Item info models"""
class ApiByLineInfo(models.ByLineInfo):
    brand: ApiSingleStringValuedAttribute
    contributors: ApiSingleStringValuedAttribute
    manufacturer: ApiSingleStringValuedAttribute

class ApiClassifications(models.Classifications):
    binding: ApiSingleStringValuedAttribute
    product_group: ApiSingleStringValuedAttribute

class ApiContentInfo(models.ContentInfo):
    edition: ApiSingleStringValuedAttribute
    languages: ApiMultiValuedAttributeType

class ApiContentRating(models.ContentRating):
    audience_rating: ApiSingleStringValuedAttribute

class ApiExternalIds(models.ExternalIds):
    ea_ns: ApiMultiValuedAttributeStr
    isb_ns: ApiMultiValuedAttributeStr
    up_cs: ApiMultiValuedAttributeStr

class ApiFeatures():
    features: ApiMultiValuedAttributeStr

class ApiManufactureInfo(models.ManufactureInfo):
    item_part_number: ApiSingleStringValuedAttribute
    model: ApiSingleStringValuedAttribute
    warranty: ApiSingleStringValuedAttribute

class ApiItemDimensions(models.DimensionBasedAttribute):
    height: ApiUnitBasedAttribute
    length: ApiUnitBasedAttribute
    weight: ApiUnitBasedAttribute
    width: ApiUnitBasedAttribute

class ApiProductInfo(models.ProductInfo):
    color: ApiSingleStringValuedAttribute
    is_adult_product: ApiSingleBooleanValuedAttribute
    item_dimensions: ApiItemDimensions
    release_date: ApiSingleStringValuedAttribute
    size: ApiSingleStringValuedAttribute
    unit_count: ApiSingleIntegerValuedAttribute

class ApiTechnicalInfo(models.TechnicalInfo):
    formats: ApiMultiValuedAttributeStr
    energy_efficiency_class: ApiSingleStringValuedAttribute

class ApiTradeInPrice(models.TradeInPrice):
    amount: float
    currency: str
    display_amount: str

class ApiTradeInInfo(models.TradeInInfo):
    is_eligible_for_trade_in: bool
    price: ApiTradeInPrice

class ApiItemInfo(models.ItemInfo):
    by_line_info: ApiByLineInfo
    classifications: ApiClassifications
    content_info: ApiContentInfo
    content_rating: ApiContentRating
    external_ids: ApiExternalIds
    features: ApiFeatures
    manufacture_info: ApiManufactureInfo
    product_info: ApiProductInfo
    technical_info: ApiTechnicalInfo
    title: ApiSingleStringValuedAttribute
    trade_in_info: ApiTradeInInfo

"""Offers model"""
class ApiOfferAvailability(models.OfferAvailability):
    max_order_quantity: int
    message: str
    min_order_quantity: int
    type: str

class ApiOfferConditionInfo:
    display_value: str
    label: str
    locale: str
    value: str

class ApiOfferSubCondition(ApiOfferConditionInfo, models.OfferSubCondition):
    pass

class ApiOfferConditionNote(models.OfferConditionNote):
    locale: str
    value: str

class ApiOfferCondition(ApiOfferConditionInfo, models.OfferCondition):
    sub_condition: ApiOfferSubCondition
    condition_note: ApiOfferConditionNote

class ApiOfferDeliveryInfo(models.OfferDeliveryInfo):
    is_amazon_fulfilled: bool
    is_free_shipping_eligible: bool
    is_prime_eligible: bool

class ApiOfferLoyaltyPoints(models.OfferLoyaltyPoints):
    points: int

class ApiOfferMerchantInfo(models.OfferMerchantInfo):
    default_shipping_country: str
    feedback_count: int
    feedback_rating: float
    id: str
    name: str

class ApiOfferSavings(ApiPrice, models.OfferSavings):
    percentage: float

class ApiOfferPrice(ApiPrice, models.OfferPrice):
    savings: models.OfferSavings

class ApiOfferProgramEligibility(models.OfferProgramEligibility):
    is_prime_exclusive: bool
    is_prime_pantry: bool

class ApiPromotion(ApiPrice, models.OfferPromotion):
    type: str
    discount_percent: float

class ApiListings(models.OfferListing):
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

class ApiOffers(models.Offers):
    listings: List[ApiListings]

"""Browse node info model"""
class ApiBrowseNode(models.BrowseNode):
    ancestor: str
    context_free_name: str
    display_name: str
    id: str
    is_root: str
    sales_rank: str

class ApiWebsiteSalesRank(models.WebsiteSalesRank):
    context_free_name: str
    display_name: str
    sales_rank: str

class ApiBrowseNodeInfo(models.BrowseNodeInfo):
    browse_nodes: List[ApiBrowseNode]
    website_sales_rank: ApiWebsiteSalesRank

"""Main model"""
class Item(models.Item):
    asin: str
    browse_node_info: ApiBrowseNodeInfo
    customer_reviews: models.CustomerReviews
    detail_page_url: str
    images: ApiImages
    item_info: ApiItemInfo
    offers: ApiOffers
    parent_asin: str
    rental_offers: models.RentalOffers
    score: float
    variation_attributes: List[models.VariationAttribute]
