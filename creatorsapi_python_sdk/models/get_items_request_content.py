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
from creatorsapi_python_sdk.models.condition import Condition
from creatorsapi_python_sdk.models.get_items_resource import GetItemsResource
from typing import Optional, Set
from typing_extensions import Self

class GetItemsRequestContent(BaseModel):
    """
    GetItemsRequestContent
    """ # noqa: E501
    partner_tag: Annotated[str, Field(strict=True, max_length=64)] = Field(description="An alphanumeric token that uniquely identifies a partner. If the value of PartnerType is Associates, enter your Store Id or tracking ID.", alias="partnerTag")
    item_ids: Annotated[List[Annotated[str, Field(strict=True)]], Field(min_length=1, max_length=10)] = Field(alias="itemIds")
    condition: Optional[Condition] = None
    currency_of_preference: Optional[Annotated[str, Field(strict=True, max_length=100)]] = Field(default=None, description="Currency of preference in which the prices information should be returned in response. By default the prices are returned in the default currency of the marketplace. Expected currency code format is the ISO 4217 currency code (i.e. USD, EUR etc.).", alias="currencyOfPreference")
    languages_of_preference: Optional[Annotated[List[Annotated[str, Field(strict=True, max_length=1000)]], Field(max_length=1)]] = Field(default=None, description="Languages in order of preference in which the item information should be returned in response. By default the item information is returned in the default language of the marketplace.", alias="languagesOfPreference")
    properties: Optional[Dict[str, Annotated[str, Field(strict=True)]]] = Field(default=None, description="Reserved parameter for specifying key-value pairs. This is a flexible mechanism for passing additional context or metadata to the API.")
    resources: Optional[Annotated[List[GetItemsResource], Field(max_length=100)]] = None
    __properties: ClassVar[List[str]] = ["partnerTag", "itemIds", "condition", "currencyOfPreference", "languagesOfPreference", "properties", "resources"]

    @field_validator('partner_tag')
    def partner_tag_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('currency_of_preference')
    def currency_of_preference_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

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
        """Create an instance of GetItemsRequestContent from a JSON string"""
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
        """Create an instance of GetItemsRequestContent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "partnerTag": obj.get("partnerTag"),
            "itemIds": obj.get("itemIds"),
            "condition": obj.get("condition"),
            "currencyOfPreference": obj.get("currencyOfPreference"),
            "languagesOfPreference": obj.get("languagesOfPreference"),
            "properties": obj.get("properties"),
            "resources": obj.get("resources")
        })
        return _obj


