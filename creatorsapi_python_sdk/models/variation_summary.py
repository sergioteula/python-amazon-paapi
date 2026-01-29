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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt
from typing import Any, ClassVar, Dict, List, Optional, Union
from creatorsapi_python_sdk.models.variation_dimension import VariationDimension
from typing import Optional, Set
from typing_extensions import Self

class VariationSummary(BaseModel):
    """
    The container for Variations Summary response. It consists of metadata of variations response like page numbers, number of variations, Price range and Variation Dimensions.
    """ # noqa: E501
    page_count: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Number of pages in the variation result set.", alias="pageCount")
    variation_count: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Total number of variations available for the product. This represents the complete count of all child ASINs across all pages. Use this value along with pageCount to understand the full scope of available variations.", alias="variationCount")
    variation_dimensions: Optional[List[VariationDimension]] = Field(default=None, description="List of variation dimensions associated with the product. Variation dimensions define the attributes on which products vary (e.g., size, color). Each dimension includes: - Display name and locale for presentation - Dimension name (internal identifier) - List of all possible values for that dimension  For example, a clothing item might have two dimensions: 'Size' with values ['S', 'M', 'L'] and 'Color' with values ['Red', 'Blue', 'Green']. These dimensions help users understand how variations differ from each other.", alias="variationDimensions")
    __properties: ClassVar[List[str]] = ["pageCount", "variationCount", "variationDimensions"]

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
        """Create an instance of VariationSummary from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in variation_dimensions (list)
        _items = []
        if self.variation_dimensions:
            for _item_variation_dimensions in self.variation_dimensions:
                if _item_variation_dimensions:
                    _items.append(_item_variation_dimensions.to_dict())
            _dict['variationDimensions'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of VariationSummary from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pageCount": obj.get("pageCount"),
            "variationCount": obj.get("variationCount"),
            "variationDimensions": [VariationDimension.from_dict(_item) for _item in obj["variationDimensions"]] if obj.get("variationDimensions") is not None else None
        })
        return _obj


