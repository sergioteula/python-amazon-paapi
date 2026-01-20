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
from creatorsapi_python_sdk.models.availability import Availability
from creatorsapi_python_sdk.models.condition import Condition
from creatorsapi_python_sdk.models.delivery_flag import DeliveryFlag
from creatorsapi_python_sdk.models.search_items_resource import SearchItemsResource
from creatorsapi_python_sdk.models.sort_by import SortBy
from typing import Optional, Set
from typing_extensions import Self

class SearchItemsRequestContent(BaseModel):
    """
    The request object for the search items operation. It contains the request parameters for the search items operation.
    """ # noqa: E501
    actor: Optional[Annotated[str, Field(strict=True, max_length=1000)]] = Field(default=None, description="Actor name associated with the item. You can enter all or part of the name.")
    artist: Optional[Annotated[str, Field(strict=True, max_length=1000)]] = Field(default=None, description="Artist name associated with the item. You can enter all or part of the name.")
    author: Optional[Annotated[str, Field(strict=True, max_length=1000)]] = Field(default=None, description="Author name associated with the item. You can enter all or part of the name.")
    availability: Optional[Availability] = None
    brand: Optional[Annotated[str, Field(strict=True, max_length=1000)]] = Field(default=None, description="Brand name associated with the item. You can enter all or part of the name.")
    browse_node_id: Optional[Annotated[str, Field(strict=True, max_length=19)]] = Field(default=None, description="A unique ID assigned by Amazon that identifies a product category/sub-category. The BrowseNodeId is a positive Long having max value upto Long.MAX_VALUE i.e. 9223372036854775807 (inclusive).", alias="browseNodeId")
    condition: Optional[Condition] = None
    currency_of_preference: Optional[Annotated[str, Field(strict=True, max_length=100)]] = Field(default=None, description="Currency of preference in which the prices information should be returned in response. By default the prices are returned in the default currency of the marketplace. Expected currency code format is the ISO 4217 currency code (i.e. USD, EUR etc.).", alias="currencyOfPreference")
    delivery_flags: Optional[Annotated[List[DeliveryFlag], Field(max_length=100)]] = Field(default=None, description="List of DeliveryFlag which denotes a certain delivery program.", alias="deliveryFlags")
    item_count: Optional[Union[Annotated[float, Field(le=100, strict=True, ge=1)], Annotated[int, Field(le=100, strict=True, ge=1)]]] = Field(default=None, description="The number of items desired in SearchItems response.", alias="itemCount")
    item_page: Optional[Union[Annotated[float, Field(le=10, strict=True, ge=1)], Annotated[int, Field(le=10, strict=True, ge=1)]]] = Field(default=None, description="The specific page of items to be returned from the available Search Results.", alias="itemPage")
    keywords: Optional[Annotated[str, Field(strict=True, max_length=1000)]] = Field(default=None, description="A word or phrase that describes an item i.e. the search query.")
    languages_of_preference: Optional[Annotated[List[Annotated[str, Field(strict=True, max_length=1000)]], Field(max_length=1)]] = Field(default=None, description="Languages in order of preference in which the item information should be returned in response. By default the item information is returned in the default language of the marketplace.", alias="languagesOfPreference")
    max_price: Optional[Union[Annotated[float, Field(strict=True, ge=1)], Annotated[int, Field(strict=True, ge=1)]]] = Field(default=None, description="The MaxPrice parameter filters search results to items with at least one offer price below the specified value.", alias="maxPrice")
    min_price: Optional[Union[Annotated[float, Field(strict=True, ge=1)], Annotated[int, Field(strict=True, ge=1)]]] = Field(default=None, description="The MinPrice parameter filters search results to items with at least one offer price above the specified value.", alias="minPrice")
    min_reviews_rating: Optional[Union[Annotated[float, Field(le=4, strict=True, ge=1)], Annotated[int, Field(le=4, strict=True, ge=1)]]] = Field(default=None, description="The MinReviewsRating parameter filters search results to items with customer review ratings above specified value.", alias="minReviewsRating")
    min_saving_percent: Optional[Union[Annotated[float, Field(le=99, strict=True, ge=1)], Annotated[int, Field(le=99, strict=True, ge=1)]]] = Field(default=None, description="The MinSavingPercent parameter filters search results to items with at least one offer having saving percentage above the specified value.", alias="minSavingPercent")
    partner_tag: Optional[Annotated[str, Field(strict=True, max_length=64)]] = Field(default=None, description="An alphanumeric token that uniquely identifies a partner. If the value of PartnerType is Associates, enter your Store Id or tracking ID.", alias="partnerTag")
    properties: Optional[Dict[str, Annotated[str, Field(strict=True)]]] = Field(default=None, description="Reserved parameter for specifying key-value pairs. This is a flexible mechanism for passing additional context or metadata to the API.")
    resources: Optional[Annotated[List[SearchItemsResource], Field(max_length=100)]] = Field(default=None, description="List of resources for SearchItems operation which specify the values to return.")
    search_index: Optional[Annotated[str, Field(strict=True, max_length=1000)]] = Field(default=None, description="Indicates the product category to search. SearchIndex values differ by marketplace.", alias="searchIndex")
    sort_by: Optional[SortBy] = Field(default=None, alias="sortBy")
    title: Optional[Annotated[str, Field(strict=True, max_length=1000)]] = Field(default=None, description="Title associated with the item.")
    __properties: ClassVar[List[str]] = ["actor", "artist", "author", "availability", "brand", "browseNodeId", "condition", "currencyOfPreference", "deliveryFlags", "itemCount", "itemPage", "keywords", "languagesOfPreference", "maxPrice", "minPrice", "minReviewsRating", "minSavingPercent", "partnerTag", "properties", "resources", "searchIndex", "sortBy", "title"]

    @field_validator('actor')
    def actor_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('artist')
    def artist_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('author')
    def author_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('brand')
    def brand_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('browse_node_id')
    def browse_node_id_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[1-9][0-9]*$", value):
            raise ValueError(r"must validate the regular expression /^[1-9][0-9]*$/")
        return value

    @field_validator('currency_of_preference')
    def currency_of_preference_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('keywords')
    def keywords_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('partner_tag')
    def partner_tag_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('search_index')
    def search_index_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r".*\S.*", value):
            raise ValueError(r"must validate the regular expression /.*\S.*/")
        return value

    @field_validator('title')
    def title_validate_regular_expression(cls, value):
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
        """Create an instance of SearchItemsRequestContent from a JSON string"""
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
        """Create an instance of SearchItemsRequestContent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "actor": obj.get("actor"),
            "artist": obj.get("artist"),
            "author": obj.get("author"),
            "availability": obj.get("availability"),
            "brand": obj.get("brand"),
            "browseNodeId": obj.get("browseNodeId"),
            "condition": obj.get("condition"),
            "currencyOfPreference": obj.get("currencyOfPreference"),
            "deliveryFlags": obj.get("deliveryFlags"),
            "itemCount": obj.get("itemCount"),
            "itemPage": obj.get("itemPage"),
            "keywords": obj.get("keywords"),
            "languagesOfPreference": obj.get("languagesOfPreference"),
            "maxPrice": obj.get("maxPrice"),
            "minPrice": obj.get("minPrice"),
            "minReviewsRating": obj.get("minReviewsRating"),
            "minSavingPercent": obj.get("minSavingPercent"),
            "partnerTag": obj.get("partnerTag"),
            "properties": obj.get("properties"),
            "resources": obj.get("resources"),
            "searchIndex": obj.get("searchIndex"),
            "sortBy": obj.get("sortBy"),
            "title": obj.get("title")
        })
        return _obj


