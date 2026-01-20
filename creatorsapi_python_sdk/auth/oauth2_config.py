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
"""

"""
OAuth2 configuration class that manages version-specific cognito endpoints
"""


class OAuth2Config:
    """OAuth2 configuration class that manages version-specific cognito endpoints"""
    
    # Constants
    SCOPE = "creatorsapi/default"
    GRANT_TYPE = "client_credentials"

    def __init__(self, credential_id, credential_secret, version, auth_endpoint):
        """
        Creates an OAuth2Config instance
        
        :param credential_id: The OAuth2 credential Id
        :param credential_secret: The OAuth2 credential secret
        :param version: The credential version (determines the token endpoint)
        :param auth_endpoint: Optional custom auth endpoint URL
        """
        self.credential_id = credential_id
        self.credential_secret = credential_secret
        self.version = version
        self.auth_endpoint = auth_endpoint
        self.cognito_endpoint = self.determine_token_endpoint(version, auth_endpoint)

    def determine_token_endpoint(self, version, auth_endpoint):
        """
        Determines the appropriate OAuth2 token endpoint based on version or custom endpoint
        
        :param version: The credential version
        :param auth_endpoint: Optional custom auth endpoint URL
        :return: The OAuth2 token endpoint URL
        :raises ValueError: If the version is not supported and no custom endpoint provided
        """
        if auth_endpoint and auth_endpoint.strip():
            return auth_endpoint
        
        # Fall back to version-based defaults
        if version == "2.1":
            return "https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token"
        elif version == "2.2":
            return "https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token"
        elif version == "2.3":
            return "https://creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token"
        else:
            raise ValueError("Unsupported version: {}. Supported versions are: 2.1, 2.2, 2.3".format(version))

    def get_token_endpoint(self, version):
        """
        Gets the appropriate OAuth2 token endpoint based on the credential version
        
        :param version: The credential version
        :return: The OAuth2 token endpoint URL
        :raises ValueError: If the version is not supported
        """
        return self.determine_token_endpoint(version, None)

    def get_credential_id(self):
        """
        Gets the credential Id
        
        :return: The credential Id
        """
        return self.credential_id

    def get_credential_secret(self):
        """
        Gets the credential secret
        
        :return: The credential secret
        """
        return self.credential_secret

    def get_version(self):
        """
        Gets the credential version
        
        :return: The credential version
        """
        return self.version

    def get_cognito_endpoint(self):
        """
        Gets the Cognito token endpoint URL
        
        :return: The token endpoint URL
        """
        return self.cognito_endpoint

    def get_scope(self):
        """
        Gets the OAuth2 scope
        
        :return: The OAuth2 scope
        """
        return OAuth2Config.SCOPE

    def get_grant_type(self):
        """
        Gets the OAuth2 grant type
        
        :return: The OAuth2 grant type
        """
        return OAuth2Config.GRANT_TYPE
