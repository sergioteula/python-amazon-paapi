"""Item result models for Amazon Product Advertising API."""

from __future__ import annotations

from amazon_paapi.sdk import models as sdk_models


class ApiLabelLocale:
    """Base class for API attributes with label and locale."""

    label: str
    locale: str


class ApiMultiValuedAttributeStr(ApiLabelLocale, sdk_models.MultiValuedAttribute):
    """Multi-valued attribute with string display values."""

    display_values: list[str]


class ApiDisplayValuesType:
    """Display value with type information."""

    display_value: str
    type: str


class ApiMultiValuedAttributeType(ApiLabelLocale, sdk_models.MultiValuedAttribute):
    """Multi-valued attribute with typed display values."""

    display_values: list[ApiDisplayValuesType]


class ApiUnitBasedAttribute(ApiLabelLocale, sdk_models.UnitBasedAttribute):
    """Unit-based attribute with numeric value and unit."""

    display_value: float
    unit: str


class ApiSingleStringValuedAttribute(
    ApiLabelLocale, sdk_models.SingleStringValuedAttribute
):
    """Single-valued attribute with string display value."""

    display_value: str


class ApiSingleBooleanValuedAttribute(
    ApiLabelLocale, sdk_models.SingleBooleanValuedAttribute
):
    """Single-valued attribute with boolean display value."""

    display_value: bool


class ApiSingleIntegerValuedAttribute(
    ApiLabelLocale, sdk_models.SingleIntegerValuedAttribute
):
    """Single-valued attribute with integer display value."""

    display_value: float


class ApiPrice:
    """Price information model."""

    amount: float
    currency: str
    price_per_unit: float
    display_amount: str
    price_type: sdk_models.PriceType
    price_type_label: str


class ApiImageSize(sdk_models.ImageSize):
    """Image size with URL and dimensions."""

    url: str
    height: str
    width: str


class ApiImageType(sdk_models.ImageType):
    """Image type with multiple size variants."""

    large: ApiImageSize
    medium: ApiImageSize
    small: ApiImageSize


class ApiImages(sdk_models.Images):
    """Container for primary and variant images."""

    primary: ApiImageType
    variants: list[ApiImageType]


class ApiByLineInfo(sdk_models.ByLineInfo):
    """Product by-line information including brand and manufacturer."""

    brand: ApiSingleStringValuedAttribute
    contributors: ApiSingleStringValuedAttribute
    manufacturer: ApiSingleStringValuedAttribute


class ApiClassifications(sdk_models.Classifications):
    """Product classification information."""

    binding: ApiSingleStringValuedAttribute
    product_group: ApiSingleStringValuedAttribute


class ApiContentInfo(sdk_models.ContentInfo):
    """Product content information."""

    edition: ApiSingleStringValuedAttribute
    languages: ApiMultiValuedAttributeType
    publication_date: ApiSingleStringValuedAttribute | None


class ApiContentRating(sdk_models.ContentRating):
    """Content rating information."""

    audience_rating: ApiSingleStringValuedAttribute


class ApiExternalIds(sdk_models.ExternalIds):
    """External product identifiers."""

    ea_ns: ApiMultiValuedAttributeStr
    isb_ns: ApiMultiValuedAttributeStr
    up_cs: ApiMultiValuedAttributeStr


class ApiFeatures:
    """Product features container."""

    features: ApiMultiValuedAttributeStr


class ApiManufactureInfo(sdk_models.ManufactureInfo):
    """Manufacturing information."""

    item_part_number: ApiSingleStringValuedAttribute
    model: ApiSingleStringValuedAttribute
    warranty: ApiSingleStringValuedAttribute


class ApiItemDimensions(sdk_models.DimensionBasedAttribute):
    """Item physical dimensions."""

    height: ApiUnitBasedAttribute
    length: ApiUnitBasedAttribute
    weight: ApiUnitBasedAttribute
    width: ApiUnitBasedAttribute


class ApiProductInfo(sdk_models.ProductInfo):
    """Product information container."""

    color: ApiSingleStringValuedAttribute
    is_adult_product: ApiSingleBooleanValuedAttribute
    item_dimensions: ApiItemDimensions
    release_date: ApiSingleStringValuedAttribute
    size: ApiSingleStringValuedAttribute
    unit_count: ApiSingleIntegerValuedAttribute


class ApiTechnicalInfo(sdk_models.TechnicalInfo):
    """Technical specifications."""

    formats: ApiMultiValuedAttributeStr
    energy_efficiency_class: ApiSingleStringValuedAttribute


class ApiTradeInPrice(sdk_models.TradeInPrice):
    """Trade-in price information."""

    amount: float
    currency: str
    display_amount: str


class ApiTradeInInfo(sdk_models.TradeInInfo):
    """Trade-in eligibility and pricing."""

    is_eligible_for_trade_in: bool
    price: ApiTradeInPrice


class ApiItemInfo(sdk_models.ItemInfo):
    """Comprehensive item information container."""

    by_line_info: ApiByLineInfo
    classifications: ApiClassifications
    content_info: ApiContentInfo | None
    content_rating: ApiContentRating
    external_ids: ApiExternalIds
    features: ApiFeatures
    manufacture_info: ApiManufactureInfo
    product_info: ApiProductInfo | None
    technical_info: ApiTechnicalInfo
    title: ApiSingleStringValuedAttribute
    trade_in_info: ApiTradeInInfo


class ApiOfferAvailability(sdk_models.OfferAvailability):
    """Offer availability information."""

    max_order_quantity: int
    message: str
    min_order_quantity: int
    type: str


class ApiOfferConditionInfo:
    """Base class for offer condition information."""

    display_value: str
    label: str
    locale: str
    value: str


class ApiOfferSubCondition(ApiOfferConditionInfo, sdk_models.OfferSubCondition):
    """Offer sub-condition details."""


class ApiOfferConditionNote(sdk_models.OfferConditionNote):
    """Offer condition note."""

    locale: str
    value: str


class ApiOfferCondition(ApiOfferConditionInfo, sdk_models.OfferCondition):
    """Offer condition with sub-condition."""

    sub_condition: ApiOfferSubCondition
    condition_note: ApiOfferConditionNote


class ApiOfferDeliveryInfo(sdk_models.OfferDeliveryInfo):
    """Offer delivery information."""

    is_amazon_fulfilled: bool
    is_free_shipping_eligible: bool
    is_prime_eligible: bool


class ApiOfferLoyaltyPoints(sdk_models.OfferLoyaltyPoints):
    """Loyalty points for offer."""

    points: int


class ApiOfferMerchantInfo(sdk_models.OfferMerchantInfo):
    """Merchant information for offer."""

    default_shipping_country: str
    feedback_count: int
    feedback_rating: float
    id: str
    name: str


class ApiOfferSavings(ApiPrice, sdk_models.OfferSavings):
    """Offer savings information."""

    percentage: float


class ApiOfferPrice(ApiPrice, sdk_models.OfferPrice):
    """Offer price with savings."""

    savings: sdk_models.OfferSavings


class ApiOfferProgramEligibility(sdk_models.OfferProgramEligibility):
    """Program eligibility for offer."""

    is_prime_exclusive: bool
    is_prime_pantry: bool


class ApiPromotion(ApiPrice, sdk_models.OfferPromotion):
    """Promotion information."""

    type: str
    discount_percent: float


class ApiListings(sdk_models.OfferListing):
    """Offer listing with all details."""

    availability: ApiOfferAvailability
    condition: ApiOfferCondition
    delivery_info: ApiOfferDeliveryInfo
    id: str
    is_buy_box_winner: bool
    loyalty_points: ApiOfferLoyaltyPoints
    merchant_info: ApiOfferMerchantInfo
    price: ApiOfferPrice
    program_eligibility: ApiOfferProgramEligibility
    promotions: list[ApiPromotion]
    saving_basis: ApiPrice
    violates_map: bool


class ApiOffers(sdk_models.Offers):
    """Container for offer listings."""

    listings: list[ApiListings]


class ApiBrowseNode(sdk_models.BrowseNode):
    """Browse node information."""

    ancestor: str
    context_free_name: str
    display_name: str
    id: str
    is_root: str
    sales_rank: str


class ApiWebsiteSalesRank(sdk_models.WebsiteSalesRank):
    """Website sales rank information."""

    context_free_name: str
    display_name: str
    sales_rank: str


class ApiBrowseNodeInfo(sdk_models.BrowseNodeInfo):
    """Browse node information container."""

    browse_nodes: list[ApiBrowseNode]
    website_sales_rank: ApiWebsiteSalesRank


class ApiMoney(sdk_models.Money):
    """Money representation for OffersV2 price fields."""

    amount: float
    currency: str
    display_amount: str


class ApiOfferAvailabilityV2(sdk_models.OfferAvailabilityV2):
    """OffersV2 availability information."""

    max_order_quantity: int
    message: str
    min_order_quantity: int
    type: str


class ApiOfferConditionV2(sdk_models.OfferConditionV2):
    """OffersV2 condition information."""

    condition_note: str
    sub_condition: str
    value: str


class ApiDealDetails(sdk_models.DealDetails):
    """Deal details for OffersV2 listings."""

    access_type: str
    badge: str
    early_access_duration_in_milliseconds: int
    end_time: str
    percent_claimed: int
    start_time: str


class ApiOfferLoyaltyPointsV2(sdk_models.OfferLoyaltyPointsV2):
    """OffersV2 loyalty points information."""

    points: int


class ApiOfferMerchantInfoV2(sdk_models.OfferMerchantInfoV2):
    """OffersV2 merchant information."""

    id: str
    name: str


class ApiOfferSavingBasis(sdk_models.OfferSavingBasis):
    """Saving basis information for OffersV2."""

    money: ApiMoney
    saving_basis_type: str
    saving_basis_type_label: str


class ApiOfferSavingsV2(sdk_models.OfferSavingsV2):
    """OffersV2 savings information."""

    money: ApiMoney
    percentage: int


class ApiOfferPriceV2(sdk_models.OfferPriceV2):
    """OffersV2 price information."""

    money: ApiMoney
    price_per_unit: ApiMoney
    saving_basis: ApiOfferSavingBasis
    savings: ApiOfferSavingsV2


class ApiListingsV2(sdk_models.OfferListingV2):
    """OffersV2 listing with all details."""

    availability: ApiOfferAvailabilityV2
    condition: ApiOfferConditionV2
    deal_details: ApiDealDetails
    is_buy_box_winner: bool
    loyalty_points: ApiOfferLoyaltyPointsV2
    merchant_info: ApiOfferMerchantInfoV2
    price: ApiOfferPriceV2
    type: sdk_models.OfferType
    violates_map: bool


class ApiOffersV2(sdk_models.OffersV2):
    """Container for OffersV2 listings."""

    listings: list[ApiListingsV2]


class Item(sdk_models.Item):
    """Amazon product item with all details."""

    asin: str
    browse_node_info: ApiBrowseNodeInfo
    customer_reviews: sdk_models.CustomerReviews
    detail_page_url: str
    images: ApiImages
    item_info: ApiItemInfo
    offers: ApiOffers
    offers_v2: ApiOffersV2
    parent_asin: str
    rental_offers: sdk_models.RentalOffers
    score: float
    variation_attributes: list[sdk_models.VariationAttribute]
