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
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from creatorsapi_python_sdk.models.condition import Condition
from creatorsapi_python_sdk.models.get_variations_resource import GetVariationsResource
from typing import Optional, Set
from typing_extensions import Self

class GetVariationsRequestContent(BaseModel):
    """
    Input for the GetVariations operation to retrieve product variation information.
    """ # noqa: E501
    partner_tag: Annotated[str, Field(strict=True, max_length=64)] = Field(description="Unique Id for a partner. This is used to identify the associate tag for tracking affiliate commissions. Example: 'xyz-20'", alias="partnerTag")
    asin: Annotated[str, Field(strict=True)] = Field(description="Amazon Standard Identification Number. This can be either a parent ASIN (to retrieve all variations) or a child ASIN (to retrieve sibling variations). Type: Non-Empty String. Example: 'B0199980K4'")
    condition: Optional[Condition] = None
    currency_of_preference: Optional[Annotated[str, Field(strict=True, max_length=100)]] = Field(default=None, description="Currency of preference in which the prices information should be returned in response. By default the prices are returned in the default currency of the marketplace. Expected currency code format is the ISO 4217 currency code (i.e. USD, EUR etc.). Example: 'USD'", alias="currencyOfPreference")
    languages_of_preference: Optional[Annotated[List[Annotated[str, Field(strict=True, max_length=1000)]], Field(max_length=1)]] = Field(default=None, description="Languages of preference in which the information should be returned in response. By default the information is returned in the default language of the marketplace. Expected locale format is the ISO 639 language code followed by underscore followed by the ISO 3166 country code (i.e. en_US, fr_CA etc.). Currently only single language of preference is supported. Example: ['en_US']", alias="languagesOfPreference")
    properties: Optional[Dict[str, Annotated[str, Field(strict=True)]]] = Field(default=None, description="Reserved parameter for specifying key-value pairs. This is a flexible mechanism for passing additional context or metadata to the API.")
    resources: Optional[Annotated[List[GetVariationsResource], Field(max_length=100)]] = Field(default=None, description="Specifies the types of values to return. You can specify multiple resources in one request. Supports high-level resources such as: - BrowseNodeInfo resources (browse nodes, ancestor, sales rank, website sales rank) - Images resources (primary and variant images in small, medium, large sizes) - ItemInfo resources (title, features, product info, technical info, etc.) - OffersV2 resources (availability, condition, price, merchant info, deal details) - VariationSummary resources (price range, variation dimensions) - ParentASIN Default: ['ItemInfo.Title']")
    variation_count: Optional[Union[Annotated[float, Field(le=10, strict=True, ge=1)], Annotated[int, Field(le=10, strict=True, ge=1)]]] = Field(default=None, description="Number of variations to be returned per page in GetVariations. By default, GetVariations returns 10 variations per page. Valid range: 1-10. Type: Positive Integer Less than or equal to 10 Default: 10 Example: 10  Use this parameter to control how many variations are returned in each response. When combined with VariationPage, you can paginate through all available variations.", alias="variationCount")
    variation_page: Optional[Union[Annotated[float, Field(strict=True, ge=1)], Annotated[int, Field(strict=True, ge=1)]]] = Field(default=None, description="Page number of variations returned by GetVariations. By default, GetVariations returns the first page. Use VariationPage to return a subsection of the response. By default, there are 10 variations per page (configurable via VariationCount). Type: Positive Integer Default: 1 Example: 1", alias="variationPage")
    __properties: ClassVar[List[str]] = ["partnerTag", "asin", "condition", "currencyOfPreference", "languagesOfPreference", "properties", "resources", "variationCount", "variationPage"]

    @field_validator('partner_tag')
    def partner_tag_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('asin')
    def asin_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[0-9]{9}[0-9X]|[A-Z][A-Z0-9]{9}$", value):
            raise ValueError(r"must validate the regular expression /^[0-9]{9}[0-9X]|[A-Z][A-Z0-9]{9}$/")
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
        """Create an instance of GetVariationsRequestContent from a JSON string"""
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
        """Create an instance of GetVariationsRequestContent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "partnerTag": obj.get("partnerTag"),
            "asin": obj.get("asin"),
            "condition": obj.get("condition"),
            "currencyOfPreference": obj.get("currencyOfPreference"),
            "languagesOfPreference": obj.get("languagesOfPreference"),
            "properties": obj.get("properties"),
            "resources": obj.get("resources"),
            "variationCount": obj.get("variationCount"),
            "variationPage": obj.get("variationPage")
        })
        return _obj


