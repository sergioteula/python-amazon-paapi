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

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from creatorsapi_python_sdk.models.get_browse_nodes_resource import GetBrowseNodesResource
from typing import Optional, Set
from typing_extensions import Self

class GetBrowseNodesRequestContent(BaseModel):
    """
    Input for the GetBrowseNodes operation to retrieve browse node information.
    """ # noqa: E501
    partner_tag: Annotated[str, Field(strict=True, max_length=64)] = Field(description="Unique ID for a partner. Type: String (Non-Empty) Default Value: None Example: 'xyz-20'", alias="partnerTag")
    browse_node_ids: Annotated[List[Annotated[str, Field(strict=True, max_length=19)]], Field(min_length=1, max_length=10)] = Field(description="List of BrowseNodeIds. A BrowseNodeId is a unique ID assigned by Amazon that identifies a product category/sub-category. The BrowseNodeId is a positive Long having max value upto Long.MAX_VALUE i.e. 9223372036854775807 (inclusive). Type: List of Strings (Positive Long only) (up to 10) Default Value: None Example: ['283155', '3040']", alias="browseNodeIds")
    languages_of_preference: Optional[Annotated[List[Annotated[str, Field(strict=True, max_length=1000)]], Field(max_length=1)]] = Field(default=None, description="Languages of preference in which the information should be returned in response. By default the information is returned in the default language of the marketplace. Expected locale format is the ISO 639 language code followed by underscore followed by the ISO 3166 country code (i.e. en_US, fr_CA etc.). Currently only single language of preference is supported. Type: List of Strings (Non-Empty) Default Value: None Example: ['en_US']", alias="languagesOfPreference")
    resources: Optional[Annotated[List[GetBrowseNodesResource], Field(max_length=100)]] = Field(default=None, description="Specifies the types of values to return. You can specify multiple resources in one request. For list of valid Resources for SearchItems operation, refer Resources Parameter. Type: List of String Default Value: ItemInfo.Title")
    __properties: ClassVar[List[str]] = ["partnerTag", "browseNodeIds", "languagesOfPreference", "resources"]

    @field_validator('partner_tag')
    def partner_tag_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

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
        """Create an instance of GetBrowseNodesRequestContent from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetBrowseNodesRequestContent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "partnerTag": obj.get("partnerTag"),
            "browseNodeIds": obj.get("browseNodeIds"),
            "languagesOfPreference": obj.get("languagesOfPreference"),
            "resources": obj.get("resources")
        })
        return _obj


