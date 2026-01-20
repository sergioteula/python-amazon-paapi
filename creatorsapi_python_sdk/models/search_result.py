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
from creatorsapi_python_sdk.models.item import Item
from creatorsapi_python_sdk.models.search_refinements import SearchRefinements
from typing import Optional, Set
from typing_extensions import Self

class SearchResult(BaseModel):
    """
    The container for SearchItems response. It consists of search results items and some meta-data about the search result like TotalResultCount, SearchURL and SearchRefinements.
    """ # noqa: E501
    total_result_count: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, alias="totalResultCount")
    search_url: Optional[StrictStr] = Field(default=None, alias="searchURL")
    items: Optional[List[Item]] = Field(default=None, description="List of Item which is a container for item information.")
    search_refinements: Optional[SearchRefinements] = Field(default=None, alias="searchRefinements")
    __properties: ClassVar[List[str]] = ["totalResultCount", "searchURL", "items", "searchRefinements"]

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
        """Create an instance of SearchResult from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in items (list)
        _items = []
        if self.items:
            for _item_items in self.items:
                if _item_items:
                    _items.append(_item_items.to_dict())
            _dict['items'] = _items
        # override the default output from pydantic by calling `to_dict()` of search_refinements
        if self.search_refinements:
            _dict['searchRefinements'] = self.search_refinements.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SearchResult from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "totalResultCount": obj.get("totalResultCount"),
            "searchURL": obj.get("searchURL"),
            "items": [Item.from_dict(_item) for _item in obj["items"]] if obj.get("items") is not None else None,
            "searchRefinements": SearchRefinements.from_dict(obj["searchRefinements"]) if obj.get("searchRefinements") is not None else None
        })
        return _obj


