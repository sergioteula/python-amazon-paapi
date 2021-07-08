from .. import models

"""Shared models"""
class ApiMultiValuedAttributeStr(models.MultiValuedAttribute):
    display_values: list[str]

class ApiDisplayValuesType:
    display_value: str
    type: str

class ApiMultiValuedAttributeType(models.MultiValuedAttribute):
    display_values: list[ApiDisplayValuesType]

"""Image models"""
class ApiImageType(models.ImageType):
    large: models.ImageSize
    medium: models.ImageSize
    small: models.ImageSize

class ApiImages(models.Images):
    primary: ApiImageType
    variants: list[ApiImageType]

"""Item info models"""
class ApiByLineInfo(models.ByLineInfo):
    brand: models.SingleStringValuedAttribute
    contributors: models.SingleStringValuedAttribute
    manufacturer: models.SingleStringValuedAttribute

class ApiClassifications(models.Classifications):
    binding: models.SingleStringValuedAttribute
    product_group: models.SingleStringValuedAttribute

class ApiContentInfo(models.ContentInfo):
    edition: models.SingleStringValuedAttribute
    languages: ApiMultiValuedAttributeType

class ApiContentRating(models.ContentRating):
    audience_rating: models.SingleStringValuedAttribute

class ApiExternalIds(models.ExternalIds):
    ea_ns: ApiMultiValuedAttributeStr
    isb_ns: ApiMultiValuedAttributeStr
    up_cs: ApiMultiValuedAttributeStr

class ApiFeatures():
    features: ApiMultiValuedAttributeStr

class ApiManufactureInfo(models.ManufactureInfo):
    item_part_number: models.SingleStringValuedAttribute
    model: models.SingleStringValuedAttribute
    warranty: models.SingleStringValuedAttribute

class ApiItemDimensions(models.DimensionBasedAttribute):
    height: models.SingleIntegerValuedAttribute
    length: models.SingleIntegerValuedAttribute
    weight: models.SingleIntegerValuedAttribute
    width: models.SingleIntegerValuedAttribute

class ApiProductInfo(models.ProductInfo):
    color: models.SingleStringValuedAttribute
    is_adult_product: models.SingleBooleanValuedAttribute
    item_dimensions: ApiItemDimensions
    release_date: models.SingleStringValuedAttribute
    size: models.SingleStringValuedAttribute
    unit_count: models.SingleIntegerValuedAttribute

class ApiTechnicalInfo(models.TechnicalInfo):
    formats: ApiMultiValuedAttributeStr
    energy_efficiency_class: models.SingleStringValuedAttribute

class ApiTradeInInfo(models.TradeInInfo):
    is_eligible_for_trade_in: bool
    price: models.TradeInPrice

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
    title: models.SingleStringValuedAttribute
    trade_in_info: ApiTradeInInfo

"""Main model"""
class ApiItem(models.Item):
    item_info: ApiItemInfo
    images: ApiImages
    offers: models.Offers
    browse_node_info: models.BrowseNodeInfo
