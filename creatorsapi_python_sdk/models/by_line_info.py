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
from creatorsapi_python_sdk.models.contributor import Contributor
from creatorsapi_python_sdk.models.single_string_valued_attribute import SingleStringValuedAttribute
from typing import Optional, Set
from typing_extensions import Self

class ByLineInfo(BaseModel):
    """
    Container for set of attributes that specifies basic information of the product like Brand, Manufacturer, etc.
    """ # noqa: E501
    brand: Optional[SingleStringValuedAttribute] = None
    contributors: Optional[List[Contributor]] = Field(default=None, description="List of contributors associated with the product.")
    manufacturer: Optional[SingleStringValuedAttribute] = None
    __properties: ClassVar[List[str]] = ["brand", "contributors", "manufacturer"]

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
        """Create an instance of ByLineInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of brand
        if self.brand:
            _dict['brand'] = self.brand.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in contributors (list)
        _items = []
        if self.contributors:
            for _item_contributors in self.contributors:
                if _item_contributors:
                    _items.append(_item_contributors.to_dict())
            _dict['contributors'] = _items
        # override the default output from pydantic by calling `to_dict()` of manufacturer
        if self.manufacturer:
            _dict['manufacturer'] = self.manufacturer.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ByLineInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "brand": SingleStringValuedAttribute.from_dict(obj["brand"]) if obj.get("brand") is not None else None,
            "contributors": [Contributor.from_dict(_item) for _item in obj["contributors"]] if obj.get("contributors") is not None else None,
            "manufacturer": SingleStringValuedAttribute.from_dict(obj["manufacturer"]) if obj.get("manufacturer") is not None else None
        })
        return _obj


