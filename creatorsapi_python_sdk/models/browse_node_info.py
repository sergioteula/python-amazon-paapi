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
from creatorsapi_python_sdk.models.browse_node import BrowseNode
from creatorsapi_python_sdk.models.website_sales_rank import WebsiteSalesRank
from typing import Optional, Set
from typing_extensions import Self

class BrowseNodeInfo(BaseModel):
    """
    Container for BrowseNode information associated with a product. Includes WebsiteSalesRank and list of BrowseNodes associated with the product.
    """ # noqa: E501
    browse_nodes: Optional[List[BrowseNode]] = Field(default=None, description="Container for list of BrowseNodes. BrowseNode contains information related to a BrowseNodeId including Id, DisplayName, ContextFreeName, IsRoot, Ancestor, Children, SalesRank associated, etc.", alias="browseNodes")
    website_sales_rank: Optional[WebsiteSalesRank] = Field(default=None, alias="websiteSalesRank")
    __properties: ClassVar[List[str]] = ["browseNodes", "websiteSalesRank"]

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
        """Create an instance of BrowseNodeInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in browse_nodes (list)
        _items = []
        if self.browse_nodes:
            for _item_browse_nodes in self.browse_nodes:
                if _item_browse_nodes:
                    _items.append(_item_browse_nodes.to_dict())
            _dict['browseNodes'] = _items
        # override the default output from pydantic by calling `to_dict()` of website_sales_rank
        if self.website_sales_rank:
            _dict['websiteSalesRank'] = self.website_sales_rank.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BrowseNodeInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "browseNodes": [BrowseNode.from_dict(_item) for _item in obj["browseNodes"]] if obj.get("browseNodes") is not None else None,
            "websiteSalesRank": WebsiteSalesRank.from_dict(obj["websiteSalesRank"]) if obj.get("websiteSalesRank") is not None else None
        })
        return _obj


