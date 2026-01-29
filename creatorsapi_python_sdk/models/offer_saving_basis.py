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
from creatorsapi_python_sdk.models.money import Money
from creatorsapi_python_sdk.models.saving_basis_type import SavingBasisType
from typing import Optional, Set
from typing_extensions import Self

class OfferSavingBasis(BaseModel):
    """
    Specifies Saving Basis of an offer
    """ # noqa: E501
    money: Optional[Money] = None
    saving_basis_type: Optional[SavingBasisType] = Field(default=None, alias="savingBasisType")
    saving_basis_type_label: Optional[StrictStr] = Field(default=None, alias="savingBasisTypeLabel")
    __properties: ClassVar[List[str]] = ["money", "savingBasisType", "savingBasisTypeLabel"]

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
        """Create an instance of OfferSavingBasis from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of money
        if self.money:
            _dict['money'] = self.money.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of OfferSavingBasis from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "money": Money.from_dict(obj["money"]) if obj.get("money") is not None else None,
            "savingBasisType": obj.get("savingBasisType"),
            "savingBasisTypeLabel": obj.get("savingBasisTypeLabel")
        })
        return _obj


