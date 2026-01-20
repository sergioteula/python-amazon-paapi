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

from pydantic import BaseModel, ConfigDict
from typing import Any, ClassVar, Dict, List, Optional
from creatorsapi_python_sdk.models.unit_based_attribute import UnitBasedAttribute
from typing import Optional, Set
from typing_extensions import Self

class DimensionBasedAttribute(BaseModel):
    """
    Container for attributes which are dimension based for example ItemDimensions, etc.
    """ # noqa: E501
    height: Optional[UnitBasedAttribute] = None
    length: Optional[UnitBasedAttribute] = None
    weight: Optional[UnitBasedAttribute] = None
    width: Optional[UnitBasedAttribute] = None
    __properties: ClassVar[List[str]] = ["height", "length", "weight", "width"]

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
        """Create an instance of DimensionBasedAttribute from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of height
        if self.height:
            _dict['height'] = self.height.to_dict()
        # override the default output from pydantic by calling `to_dict()` of length
        if self.length:
            _dict['length'] = self.length.to_dict()
        # override the default output from pydantic by calling `to_dict()` of weight
        if self.weight:
            _dict['weight'] = self.weight.to_dict()
        # override the default output from pydantic by calling `to_dict()` of width
        if self.width:
            _dict['width'] = self.width.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DimensionBasedAttribute from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "height": UnitBasedAttribute.from_dict(obj["height"]) if obj.get("height") is not None else None,
            "length": UnitBasedAttribute.from_dict(obj["length"]) if obj.get("length") is not None else None,
            "weight": UnitBasedAttribute.from_dict(obj["weight"]) if obj.get("weight") is not None else None,
            "width": UnitBasedAttribute.from_dict(obj["width"]) if obj.get("width") is not None else None
        })
        return _obj


