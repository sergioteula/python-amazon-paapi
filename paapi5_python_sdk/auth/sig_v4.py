# coding: utf-8

"""
 Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License").
 You may not use this file except in compliance with the License.
 A copy of the License is located at

     http://www.apache.org/licenses/LICENSE-2.0

 or in the "license" file accompanying this file. This file is distributed
 on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 express or implied. See the License for the specific language governing
 permissions and limitations under the License.
"""

"""
ProductAdvertisingAPI
 
https://webservices.amazon.com/paapi5/documentation/index.html
 
"""

import hashlib
import hmac
import json


class AWSV4Auth:
    def __init__(
        self,
        access_key,
        secret_key,
        host,
        region,
        service,
        method_name,
        timestamp,
        headers={},
        path="",
        payload="",
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.host = host
        self.region = region
        self.service = service
        self.method_name = method_name
        self.headers = headers
        self.timestamp = timestamp
        self.payload = payload
        self.path = path

        self.xAmzDateTime = self.timestamp.strftime("%Y%m%dT%H%M%SZ")
        self.xAmzDate = self.timestamp.strftime("%Y%m%d")

    def getHeaders(self):
        canonical_request = self.prepareCanonicalURL()
        string_to_sign = self.prepareStringToSign(canonical_request=canonical_request)
        signing_key = self.getSignatureKey(
            self.secret_key, self.xAmzDate, self.region, self.service
        )
        signature = self.getSignature(
            signing_key=signing_key, string_to_sign=string_to_sign
        )

        authorization_header = (
            self.algorithm
            + " "
            + "Credential="
            + self.access_key
            + "/"
            + self.credential_scope
            + ", "
            + "SignedHeaders="
            + self.signed_header
            + ", "
            + "Signature="
            + signature
        )
        self.headers["Authorization"] = authorization_header
        return self.headers

    def prepareCanonicalURL(self):
        canonical_uri = self.method_name + "\n" + self.path
        canonical_querystring = ""
        canonical_header = ""
        self.signed_header = ""
        sortedkeys = sorted(self.headers, key=str.lower)
        for key in sortedkeys:
            self.signed_header = self.signed_header + key.lower() + ";"
            canonical_header = (
                canonical_header + key.lower() + ":" + self.headers[key] + "\n"
            )
        self.signed_header = self.signed_header[:-1]
        payload_hash = hashlib.sha256(
            json.dumps(self.payload).encode("utf-8")
        ).hexdigest()
        canonical_request = (
            canonical_uri
            + "\n"
            + canonical_querystring
            + "\n"
            + canonical_header
            + "\n"
            + self.signed_header
            + "\n"
            + payload_hash
        )
        return canonical_request

    def prepareStringToSign(self, canonical_request):
        self.algorithm = "AWS4-HMAC-SHA256"
        self.credential_scope = (
            self.xAmzDate
            + "/"
            + self.region
            + "/"
            + self.service
            + "/"
            + "aws4_request"
        )
        string_to_sign = (
            self.algorithm
            + "\n"
            + self.xAmzDateTime
            + "\n"
            + self.credential_scope
            + "\n"
            + hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        )
        return string_to_sign

    def sign(self, key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def getSignatureKey(self, key, dateStamp, regionName, serviceName):
        kDate = self.sign(("AWS4" + key).encode("utf-8"), dateStamp)
        kRegion = self.sign(kDate, regionName)
        kService = self.sign(kRegion, serviceName)
        kSigning = self.sign(kService, "aws4_request")
        return kSigning

    def getSignature(self, signing_key, string_to_sign):
        signature = hmac.new(
            signing_key, (string_to_sign).encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return signature
