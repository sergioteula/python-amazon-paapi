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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from creatorsapi_python_sdk.models.by_line_info import ByLineInfo
from creatorsapi_python_sdk.models.classifications import Classifications
from creatorsapi_python_sdk.models.content_info import ContentInfo
from creatorsapi_python_sdk.models.content_rating import ContentRating
from creatorsapi_python_sdk.models.external_ids import ExternalIds
from creatorsapi_python_sdk.models.manufacture_info import ManufactureInfo
from creatorsapi_python_sdk.models.multi_valued_attribute import MultiValuedAttribute
from creatorsapi_python_sdk.models.product_info import ProductInfo
from creatorsapi_python_sdk.models.single_string_valued_attribute import SingleStringValuedAttribute
from creatorsapi_python_sdk.models.technical_info import TechnicalInfo
from creatorsapi_python_sdk.models.trade_in_info import TradeInInfo
from typing import Optional, Set
from typing_extensions import Self

class ItemInfo(BaseModel):
    """
    Container for ItemInfo high level resource which is a collection of large number of attributes describing a product.
    """ # noqa: E501
    by_line_info: Optional[ByLineInfo] = Field(default=None, alias="byLineInfo")
    classifications: Optional[Classifications] = None
    content_info: Optional[ContentInfo] = Field(default=None, alias="contentInfo")
    content_rating: Optional[ContentRating] = Field(default=None, alias="contentRating")
    external_ids: Optional[ExternalIds] = Field(default=None, alias="externalIds")
    features: Optional[MultiValuedAttribute] = None
    manufacture_info: Optional[ManufactureInfo] = Field(default=None, alias="manufactureInfo")
    product_info: Optional[ProductInfo] = Field(default=None, alias="productInfo")
    technical_info: Optional[TechnicalInfo] = Field(default=None, alias="technicalInfo")
    title: Optional[SingleStringValuedAttribute] = None
    trade_in_info: Optional[TradeInInfo] = Field(default=None, alias="tradeInInfo")
    __properties: ClassVar[List[str]] = ["byLineInfo", "classifications", "contentInfo", "contentRating", "externalIds", "features", "manufactureInfo", "productInfo", "technicalInfo", "title", "tradeInInfo"]

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
        """Create an instance of ItemInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of by_line_info
        if self.by_line_info:
            _dict['byLineInfo'] = self.by_line_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of classifications
        if self.classifications:
            _dict['classifications'] = self.classifications.to_dict()
        # override the default output from pydantic by calling `to_dict()` of content_info
        if self.content_info:
            _dict['contentInfo'] = self.content_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of content_rating
        if self.content_rating:
            _dict['contentRating'] = self.content_rating.to_dict()
        # override the default output from pydantic by calling `to_dict()` of external_ids
        if self.external_ids:
            _dict['externalIds'] = self.external_ids.to_dict()
        # override the default output from pydantic by calling `to_dict()` of features
        if self.features:
            _dict['features'] = self.features.to_dict()
        # override the default output from pydantic by calling `to_dict()` of manufacture_info
        if self.manufacture_info:
            _dict['manufactureInfo'] = self.manufacture_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of product_info
        if self.product_info:
            _dict['productInfo'] = self.product_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of technical_info
        if self.technical_info:
            _dict['technicalInfo'] = self.technical_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of title
        if self.title:
            _dict['title'] = self.title.to_dict()
        # override the default output from pydantic by calling `to_dict()` of trade_in_info
        if self.trade_in_info:
            _dict['tradeInInfo'] = self.trade_in_info.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ItemInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "byLineInfo": ByLineInfo.from_dict(obj["byLineInfo"]) if obj.get("byLineInfo") is not None else None,
            "classifications": Classifications.from_dict(obj["classifications"]) if obj.get("classifications") is not None else None,
            "contentInfo": ContentInfo.from_dict(obj["contentInfo"]) if obj.get("contentInfo") is not None else None,
            "contentRating": ContentRating.from_dict(obj["contentRating"]) if obj.get("contentRating") is not None else None,
            "externalIds": ExternalIds.from_dict(obj["externalIds"]) if obj.get("externalIds") is not None else None,
            "features": MultiValuedAttribute.from_dict(obj["features"]) if obj.get("features") is not None else None,
            "manufactureInfo": ManufactureInfo.from_dict(obj["manufactureInfo"]) if obj.get("manufactureInfo") is not None else None,
            "productInfo": ProductInfo.from_dict(obj["productInfo"]) if obj.get("productInfo") is not None else None,
            "technicalInfo": TechnicalInfo.from_dict(obj["technicalInfo"]) if obj.get("technicalInfo") is not None else None,
            "title": SingleStringValuedAttribute.from_dict(obj["title"]) if obj.get("title") is not None else None,
            "tradeInInfo": TradeInInfo.from_dict(obj["tradeInInfo"]) if obj.get("tradeInInfo") is not None else None
        })
        return _obj


