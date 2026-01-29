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
from creatorsapi_python_sdk.models.image_size import ImageSize
from typing import Optional, Set
from typing_extensions import Self

class ImageType(BaseModel):
    """
    Container for image sizes associated with an image type. Images are returned in various sizes like small, medium and large.
    """ # noqa: E501
    small: Optional[ImageSize] = None
    medium: Optional[ImageSize] = None
    large: Optional[ImageSize] = None
    hi_res: Optional[ImageSize] = Field(default=None, alias="hiRes")
    __properties: ClassVar[List[str]] = ["small", "medium", "large", "hiRes"]

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
        """Create an instance of ImageType from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of small
        if self.small:
            _dict['small'] = self.small.to_dict()
        # override the default output from pydantic by calling `to_dict()` of medium
        if self.medium:
            _dict['medium'] = self.medium.to_dict()
        # override the default output from pydantic by calling `to_dict()` of large
        if self.large:
            _dict['large'] = self.large.to_dict()
        # override the default output from pydantic by calling `to_dict()` of hi_res
        if self.hi_res:
            _dict['hiRes'] = self.hi_res.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ImageType from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "small": ImageSize.from_dict(obj["small"]) if obj.get("small") is not None else None,
            "medium": ImageSize.from_dict(obj["medium"]) if obj.get("medium") is not None else None,
            "large": ImageSize.from_dict(obj["large"]) if obj.get("large") is not None else None,
            "hiRes": ImageSize.from_dict(obj["hiRes"]) if obj.get("hiRes") is not None else None
        })
        return _obj


