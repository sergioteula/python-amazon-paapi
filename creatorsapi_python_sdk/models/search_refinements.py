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
from creatorsapi_python_sdk.models.refinement import Refinement
from typing import Optional, Set
from typing_extensions import Self

class SearchRefinements(BaseModel):
    """
    Container for SearchRefinements resource which helps in filtering search results obtained from SearchItems operation. It contains relevant SearchIndexes, BrowseNodes and other dynamic refinements for a search request.
    """ # noqa: E501
    browse_node: Optional[Refinement] = Field(default=None, alias="browseNode")
    other_refinements: Optional[List[Refinement]] = Field(default=None, description="List of refinements.", alias="otherRefinements")
    search_index: Optional[Refinement] = Field(default=None, alias="searchIndex")
    __properties: ClassVar[List[str]] = ["browseNode", "otherRefinements", "searchIndex"]

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
        """Create an instance of SearchRefinements from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of browse_node
        if self.browse_node:
            _dict['browseNode'] = self.browse_node.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in other_refinements (list)
        _items = []
        if self.other_refinements:
            for _item_other_refinements in self.other_refinements:
                if _item_other_refinements:
                    _items.append(_item_other_refinements.to_dict())
            _dict['otherRefinements'] = _items
        # override the default output from pydantic by calling `to_dict()` of search_index
        if self.search_index:
            _dict['searchIndex'] = self.search_index.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SearchRefinements from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "browseNode": Refinement.from_dict(obj["browseNode"]) if obj.get("browseNode") is not None else None,
            "otherRefinements": [Refinement.from_dict(_item) for _item in obj["otherRefinements"]] if obj.get("otherRefinements") is not None else None,
            "searchIndex": Refinement.from_dict(obj["searchIndex"]) if obj.get("searchIndex") is not None else None
        })
        return _obj


