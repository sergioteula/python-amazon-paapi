from .. import models


class ApiImageType(models.ImageType):
    large: models.ImageSize
    medium: models.ImageSize
    small: models.ImageSize


class ApiImages(models.Images):
    primary: ApiImageType
    variants: list[ApiImageType]


class ApiByLineInfo(models.ByLineInfo):
    brand: models.SingleStringValuedAttribute
    contributors: models.SingleStringValuedAttribute
    manufacturer: models.SingleStringValuedAttribute


class ApiClassifications(models.Classifications):
    binding: models.SingleStringValuedAttribute
    product_group: models.SingleStringValuedAttribute


class ApiContentInfo(models.ContentInfo):
    edition: models.SingleStringValuedAttribute
    languages: models.MultiValuedAttribute


class ApiItemInfo(models.ItemInfo):
    by_line_info: ApiByLineInfo
    classifications: ApiClassifications
    content_info: ApiContentInfo


class ApiItem(models.Item):
    item_info: ApiItemInfo
    images: ApiImages
    offers: models.Offers
    browse_node_info: models.BrowseNodeInfo
