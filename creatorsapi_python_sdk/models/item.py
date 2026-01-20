# coding: utf-8

"""
Copyright 2025 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

    http://www.apache.org/licenses/LICENSE-2.0

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.

"""  # noqa: E501



from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from creatorsapi_python_sdk.models.browse_node_info import BrowseNodeInfo
from creatorsapi_python_sdk.models.customer_reviews import CustomerReviews
from creatorsapi_python_sdk.models.images import Images
from creatorsapi_python_sdk.models.item_info import ItemInfo
from creatorsapi_python_sdk.models.offers_v2 import OffersV2
from creatorsapi_python_sdk.models.variation_attribute import VariationAttribute
from typing import Optional, Set
from typing_extensions import Self

class Item(BaseModel):
    """
    Container for item information such as ASIN, Detail Page URL and other attributes. It also includes containers for various item related resources like Images, ItemInfo, etc.
    """ # noqa: E501
    asin: Optional[StrictStr] = None
    browse_node_info: Optional[BrowseNodeInfo] = Field(default=None, alias="browseNodeInfo")
    customer_reviews: Optional[CustomerReviews] = Field(default=None, alias="customerReviews")
    detail_page_url: Optional[StrictStr] = Field(default=None, alias="detailPageURL")
    images: Optional[Images] = None
    item_info: Optional[ItemInfo] = Field(default=None, alias="itemInfo")
    offers_v2: Optional[OffersV2] = Field(default=None, alias="offersV2")
    parent_asin: Optional[StrictStr] = Field(default=None, alias="parentASIN")
    score: Optional[Union[StrictFloat, StrictInt]] = None
    variation_attributes: Optional[List[VariationAttribute]] = Field(default=None, description="List of offer listing associated with a product.", alias="variationAttributes")
    __properties: ClassVar[List[str]] = ["asin", "browseNodeInfo", "customerReviews", "detailPageURL", "images", "itemInfo", "offersV2", "parentASIN", "score", "variationAttributes"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return self.model_dump_json(by_alias=True, exclude_unset=True)

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Item from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of browse_node_info
        if self.browse_node_info:
            _dict['browseNodeInfo'] = self.browse_node_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of customer_reviews
        if self.customer_reviews:
            _dict['customerReviews'] = self.customer_reviews.to_dict()
        # override the default output from pydantic by calling `to_dict()` of images
        if self.images:
            _dict['images'] = self.images.to_dict()
        # override the default output from pydantic by calling `to_dict()` of item_info
        if self.item_info:
            _dict['itemInfo'] = self.item_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of offers_v2
        if self.offers_v2:
            _dict['offersV2'] = self.offers_v2.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in variation_attributes (list)
        _items = []
        if self.variation_attributes:
            for _item_variation_attributes in self.variation_attributes:
                if _item_variation_attributes:
                    _items.append(_item_variation_attributes.to_dict())
            _dict['variationAttributes'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Item from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "asin": obj.get("asin"),
            "browseNodeInfo": BrowseNodeInfo.from_dict(obj["browseNodeInfo"]) if obj.get("browseNodeInfo") is not None else None,
            "customerReviews": CustomerReviews.from_dict(obj["customerReviews"]) if obj.get("customerReviews") is not None else None,
            "detailPageURL": obj.get("detailPageURL"),
            "images": Images.from_dict(obj["images"]) if obj.get("images") is not None else None,
            "itemInfo": ItemInfo.from_dict(obj["itemInfo"]) if obj.get("itemInfo") is not None else None,
            "offersV2": OffersV2.from_dict(obj["offersV2"]) if obj.get("offersV2") is not None else None,
            "parentASIN": obj.get("parentASIN"),
            "score": obj.get("score"),
            "variationAttributes": [VariationAttribute.from_dict(_item) for _item in obj["variationAttributes"]] if obj.get("variationAttributes") is not None else None
        })
        return _obj


