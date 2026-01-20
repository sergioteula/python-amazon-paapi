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
from creatorsapi_python_sdk.models.dimension_based_attribute import DimensionBasedAttribute
from creatorsapi_python_sdk.models.single_boolean_valued_attribute import SingleBooleanValuedAttribute
from creatorsapi_python_sdk.models.single_integer_valued_attribute import SingleIntegerValuedAttribute
from creatorsapi_python_sdk.models.single_string_valued_attribute import SingleStringValuedAttribute
from typing import Optional, Set
from typing_extensions import Self

class ProductInfo(BaseModel):
    """
    Container for set of attributes that describes non-technical aspects of the product.
    """ # noqa: E501
    color: Optional[SingleStringValuedAttribute] = None
    is_adult_product: Optional[SingleBooleanValuedAttribute] = Field(default=None, alias="isAdultProduct")
    item_dimensions: Optional[DimensionBasedAttribute] = Field(default=None, alias="itemDimensions")
    release_date: Optional[SingleStringValuedAttribute] = Field(default=None, alias="releaseDate")
    size: Optional[SingleStringValuedAttribute] = None
    unit_count: Optional[SingleIntegerValuedAttribute] = Field(default=None, alias="unitCount")
    __properties: ClassVar[List[str]] = ["color", "isAdultProduct", "itemDimensions", "releaseDate", "size", "unitCount"]

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
        """Create an instance of ProductInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of color
        if self.color:
            _dict['color'] = self.color.to_dict()
        # override the default output from pydantic by calling `to_dict()` of is_adult_product
        if self.is_adult_product:
            _dict['isAdultProduct'] = self.is_adult_product.to_dict()
        # override the default output from pydantic by calling `to_dict()` of item_dimensions
        if self.item_dimensions:
            _dict['itemDimensions'] = self.item_dimensions.to_dict()
        # override the default output from pydantic by calling `to_dict()` of release_date
        if self.release_date:
            _dict['releaseDate'] = self.release_date.to_dict()
        # override the default output from pydantic by calling `to_dict()` of size
        if self.size:
            _dict['size'] = self.size.to_dict()
        # override the default output from pydantic by calling `to_dict()` of unit_count
        if self.unit_count:
            _dict['unitCount'] = self.unit_count.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProductInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "color": SingleStringValuedAttribute.from_dict(obj["color"]) if obj.get("color") is not None else None,
            "isAdultProduct": SingleBooleanValuedAttribute.from_dict(obj["isAdultProduct"]) if obj.get("isAdultProduct") is not None else None,
            "itemDimensions": DimensionBasedAttribute.from_dict(obj["itemDimensions"]) if obj.get("itemDimensions") is not None else None,
            "releaseDate": SingleStringValuedAttribute.from_dict(obj["releaseDate"]) if obj.get("releaseDate") is not None else None,
            "size": SingleStringValuedAttribute.from_dict(obj["size"]) if obj.get("size") is not None else None,
            "unitCount": SingleIntegerValuedAttribute.from_dict(obj["unitCount"]) if obj.get("unitCount") is not None else None
        })
        return _obj


