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
import json
from enum import Enum
from typing_extensions import Self


class ValidationExceptionReason(str, Enum):
    """
    Possible reasons a request failed validation
    """

    """
    allowed enum values
    """
    UNKNOWNOPERATION = 'UnknownOperation'
    CANNOTPARSE = 'CannotParse'
    FIELDVALIDATIONFAILED = 'FieldValidationFailed'
    INVALIDASSOCIATE = 'InvalidAssociate'
    INVALIDPARTNERTAG = 'InvalidPartnerTag'
    OTHER = 'Other'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ValidationExceptionReason from a JSON string"""
        return cls(json.loads(json_str))



