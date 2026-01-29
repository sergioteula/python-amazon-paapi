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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from creatorsapi_python_sdk.models.browse_node_ancestor import BrowseNodeAncestor
from creatorsapi_python_sdk.models.browse_node_child import BrowseNodeChild
from typing import Optional, Set
from typing_extensions import Self

class BrowseNode(BaseModel):
    """
    Container for BrowseNode information which includes BrowseNodeId, DisplayName, ContextFreeName, IsRoot, Ancestor, Children, SalesRank associated, etc.
    """ # noqa: E501
    ancestor: Optional[BrowseNodeAncestor] = None
    children: Optional[List[BrowseNodeChild]] = Field(default=None, description="List of BrowseNode Children for a particular BrowseNode.")
    context_free_name: Optional[StrictStr] = Field(default=None, description="Indicates a displayable name for a BrowseNode that is fully context free. For e.g. DisplayName of BrowseNodeId: 3060 in US marketplace is 'Orphans & Foster Homes'. One can not infer which root category this browse node belongs to unless we have the ancestry ladder for this browse node i.e. it requires a 'context' for being intuitive. However, the ContextFreeName of this browse node is 'Children's Orphans & Foster Homes Books'. Note that, for a BrowseNode whose DisplayName is already context free will have the same ContextFreeName as DisplayName.", alias="contextFreeName")
    display_name: Optional[StrictStr] = Field(default=None, description="The display name of the BrowseNode as visible on the Amazon retail website.", alias="displayName")
    id: Optional[StrictStr] = Field(default=None, description="Indicates the unique identifier of the BrowseNode")
    is_root: Optional[StrictBool] = Field(default=None, description="Indicates if the current BrowseNode is a root category.", alias="isRoot")
    sales_rank: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, alias="salesRank")
    __properties: ClassVar[List[str]] = ["ancestor", "children", "contextFreeName", "displayName", "id", "isRoot", "salesRank"]

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
        """Create an instance of BrowseNode from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in children (list)
        _items = []
        if self.children:
            for _item_children in self.children:
                if _item_children:
                    _items.append(_item_children.to_dict())
            _dict['children'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BrowseNode from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "ancestor": BrowseNodeAncestor.from_dict(obj["ancestor"]) if obj.get("ancestor") is not None else None,
            "children": [BrowseNodeChild.from_dict(_item) for _item in obj["children"]] if obj.get("children") is not None else None,
            "contextFreeName": obj.get("contextFreeName"),
            "displayName": obj.get("displayName"),
            "id": obj.get("id"),
            "isRoot": obj.get("isRoot"),
            "salesRank": obj.get("salesRank")
        })
        return _obj


