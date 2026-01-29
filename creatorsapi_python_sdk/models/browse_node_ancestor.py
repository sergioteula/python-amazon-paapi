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
from typing import Optional, Set
from typing_extensions import Self

class BrowseNodeAncestor(BaseModel):
    """
    Container for BrowseNode Ancestor information which includes BrowseNodeId, DisplayName, ContextFreeName and Ancestor information if one exists. The container is a ladder containing ancestor information up-to root browse node. That is, the last node in the ladder will be Root Node. Note that a root BrowseNode will not have any ancestor.
    """ # noqa: E501
    ancestor: Optional[BrowseNodeAncestor] = None
    context_free_name: Optional[StrictStr] = Field(default=None, alias="contextFreeName")
    display_name: Optional[StrictStr] = Field(default=None, alias="displayName")
    id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["ancestor", "contextFreeName", "displayName", "id"]

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
        """Create an instance of BrowseNodeAncestor from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of ancestor
        if self.ancestor:
            _dict['ancestor'] = self.ancestor.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BrowseNodeAncestor from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "ancestor": BrowseNodeAncestor.from_dict(obj["ancestor"]) if obj.get("ancestor") is not None else None,
            "contextFreeName": obj.get("contextFreeName"),
            "displayName": obj.get("displayName"),
            "id": obj.get("id")
        })
        return _obj

# TODO: Rewrite to not use raise_errors
BrowseNodeAncestor.model_rebuild(raise_errors=False)

