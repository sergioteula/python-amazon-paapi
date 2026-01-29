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
from creatorsapi_python_sdk.models.single_string_valued_attribute import SingleStringValuedAttribute
from typing import Optional, Set
from typing_extensions import Self

class ManufactureInfo(BaseModel):
    """
    Container for set of attributes that specifies manufacturing related information of a product.
    """ # noqa: E501
    item_part_number: Optional[SingleStringValuedAttribute] = Field(default=None, alias="itemPartNumber")
    model: Optional[SingleStringValuedAttribute] = None
    warranty: Optional[SingleStringValuedAttribute] = None
    __properties: ClassVar[List[str]] = ["itemPartNumber", "model", "warranty"]

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
        """Create an instance of ManufactureInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of item_part_number
        if self.item_part_number:
            _dict['itemPartNumber'] = self.item_part_number.to_dict()
        # override the default output from pydantic by calling `to_dict()` of model
        if self.model:
            _dict['model'] = self.model.to_dict()
        # override the default output from pydantic by calling `to_dict()` of warranty
        if self.warranty:
            _dict['warranty'] = self.warranty.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ManufactureInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "itemPartNumber": SingleStringValuedAttribute.from_dict(obj["itemPartNumber"]) if obj.get("itemPartNumber") is not None else None,
            "model": SingleStringValuedAttribute.from_dict(obj["model"]) if obj.get("model") is not None else None,
            "warranty": SingleStringValuedAttribute.from_dict(obj["warranty"]) if obj.get("warranty") is not None else None
        })
        return _obj


