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


class ReportType(str, Enum):
    """
    The source program a report belongs to. Stamped on ListReports response entries under the enforced treatment so callers can distinguish Creator Central from Creator Connections reports and route GetReport explicitly.
    """

    """
    allowed enum values
    """
    CREATOR_CENTRAL = 'CREATOR_CENTRAL'
    CREATOR_CONNECTIONS = 'CREATOR_CONNECTIONS'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ReportType from a JSON string"""
        return cls(json.loads(json_str))



