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

from pydantic import BaseModel, ConfigDict, Field, StrictBool
from typing import Any, ClassVar, Dict, List, Optional
from creatorsapi_python_sdk.models.deal_details import DealDetails
from creatorsapi_python_sdk.models.offer_availability_v2 import OfferAvailabilityV2
from creatorsapi_python_sdk.models.offer_condition_v2 import OfferConditionV2
from creatorsapi_python_sdk.models.offer_loyalty_points_v2 import OfferLoyaltyPointsV2
from creatorsapi_python_sdk.models.offer_merchant_info_v2 import OfferMerchantInfoV2
from creatorsapi_python_sdk.models.offer_price_v2 import OfferPriceV2
from creatorsapi_python_sdk.models.offer_type import OfferType
from typing import Optional, Set
from typing_extensions import Self

class OfferListingV2(BaseModel):
    """
    Specifies about various offer listings associated with the product.
    """ # noqa: E501
    availability: Optional[OfferAvailabilityV2] = None
    condition: Optional[OfferConditionV2] = None
    deal_details: Optional[DealDetails] = Field(default=None, alias="dealDetails")
    is_buy_box_winner: Optional[StrictBool] = Field(default=None, alias="isBuyBoxWinner")
    loyalty_points: Optional[OfferLoyaltyPointsV2] = Field(default=None, alias="loyaltyPoints")
    merchant_info: Optional[OfferMerchantInfoV2] = Field(default=None, alias="merchantInfo")
    price: Optional[OfferPriceV2] = None
    type: Optional[OfferType] = None
    violates_map: Optional[StrictBool] = Field(default=None, alias="violatesMAP")
    __properties: ClassVar[List[str]] = ["availability", "condition", "dealDetails", "isBuyBoxWinner", "loyaltyPoints", "merchantInfo", "price", "type", "violatesMAP"]

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
        """Create an instance of OfferListingV2 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of availability
        if self.availability:
            _dict['availability'] = self.availability.to_dict()
        # override the default output from pydantic by calling `to_dict()` of condition
        if self.condition:
            _dict['condition'] = self.condition.to_dict()
        # override the default output from pydantic by calling `to_dict()` of deal_details
        if self.deal_details:
            _dict['dealDetails'] = self.deal_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of loyalty_points
        if self.loyalty_points:
            _dict['loyaltyPoints'] = self.loyalty_points.to_dict()
        # override the default output from pydantic by calling `to_dict()` of merchant_info
        if self.merchant_info:
            _dict['merchantInfo'] = self.merchant_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of price
        if self.price:
            _dict['price'] = self.price.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of OfferListingV2 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "availability": OfferAvailabilityV2.from_dict(obj["availability"]) if obj.get("availability") is not None else None,
            "condition": OfferConditionV2.from_dict(obj["condition"]) if obj.get("condition") is not None else None,
            "dealDetails": DealDetails.from_dict(obj["dealDetails"]) if obj.get("dealDetails") is not None else None,
            "isBuyBoxWinner": obj.get("isBuyBoxWinner"),
            "loyaltyPoints": OfferLoyaltyPointsV2.from_dict(obj["loyaltyPoints"]) if obj.get("loyaltyPoints") is not None else None,
            "merchantInfo": OfferMerchantInfoV2.from_dict(obj["merchantInfo"]) if obj.get("merchantInfo") is not None else None,
            "price": OfferPriceV2.from_dict(obj["price"]) if obj.get("price") is not None else None,
            "type": obj.get("type"),
            "violatesMAP": obj.get("violatesMAP")
        })
        return _obj


