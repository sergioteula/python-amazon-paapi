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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from creatorsapi_python_sdk.models.refinement_bin import RefinementBin
from typing import Optional, Set
from typing_extensions import Self

class Refinement(BaseModel):
    """
    Container for a search refinement which includes refinement attributes like Id, Display Name and refinement values.
    """ # noqa: E501
    bins: Optional[List[RefinementBin]] = Field(default=None, description="List of refinement bins which contains the values for a particular refinement.")
    display_name: Optional[StrictStr] = Field(default=None, alias="displayName")
    id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["bins", "displayName", "id"]

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
        """Create an instance of Refinement from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in bins (list)
        _items = []
        if self.bins:
            for _item_bins in self.bins:
                if _item_bins:
                    _items.append(_item_bins.to_dict())
            _dict['bins'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Refinement from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "bins": [RefinementBin.from_dict(_item) for _item in obj["bins"]] if obj.get("bins") is not None else None,
            "displayName": obj.get("displayName"),
            "id": obj.get("id")
        })
        return _obj


