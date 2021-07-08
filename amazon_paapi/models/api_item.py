from .. import models

"""Shared models"""
class ApiLabelLocale:
    label: str
    locale: str

class ApiMultiValuedAttributeStr(ApiLabelLocale, models.MultiValuedAttribute):
    display_values: list[str]

class ApiDisplayValuesType:
    display_value: str
    type: str

class ApiMultiValuedAttributeType(ApiLabelLocale, models.MultiValuedAttribute):
    display_values: list[ApiDisplayValuesType]

class ApiUnitBasedAttribute(ApiLabelLocale, models.UnitBasedAttribute):
    display_value: float
    unit: str

class ApiSingleStringValuedAttribute(ApiLabelLocale, models.SingleStringValuedAttribute):
    display_value: str

class ApiSingleBooleanValuedAttribute(ApiLabelLocale, models.SingleBooleanValuedAttribute):
    display_value: bool

class ApiSingleIntegerValuedAttribute(ApiLabelLocale, models.SingleIntegerValuedAttribute):
    display_value: float

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
    variants: list[ApiImageType]

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
class ApiOfferCondition(models.OfferCondition):
    sub_condition: models.OfferSubCondition
    condition_note: models.OfferConditionNote

class ApiListings(models.OfferListing):
    availability: models.Availability
    condition: ApiOfferCondition
    delivery_info: models.OfferDeliveryInfo
    id: str
    is_buy_box_winner: bool


class ApiOffers(models.Offers):
    listings: list[ApiListings]


"""Browse node info model"""
class ApiBrowseNodeInfo(models.BrowseNodeInfo):
    pass

"""Main model"""
class ApiItem(models.Item):
    item_info: ApiItemInfo
    images: ApiImages
    offers: ApiOffers
    browse_node_info: ApiBrowseNodeInfo
