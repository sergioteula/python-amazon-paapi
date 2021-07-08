from .. import models


class ApiImageType(models.ImageType):
    large: models.ImageSize
    medium: models.ImageSize
    small: models.ImageSize


class ApiImages(models.Images):
    primary: ApiImageType
    variants: list[ApiImageType]


class AmazonItem(models.Item):
    item_info: models.ItemInfo
    images: ApiImages
    offers: models.Offers
    browse_node_info: models.BrowseNodeInfo

    models.Images.primary
