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
OAuth2 Token Manager for handling token refresh and caching.

Note: ApiClient automatically manages token caching for optimal performance.
Direct instantiation is only needed for advanced use cases.
"""

import requests
import time
import json


class OAuth2TokenManager:
    """Manages OAuth2 token lifecycle including acquisition, caching, and automatic refresh"""

    def __init__(self, config):
        """
        Creates an OAuth2TokenManager instance
        
        :param config: The OAuth2Config instance
        """
        self.config = config
        self.access_token = None
        self.expires_at = None

    def get_token(self):
        """
        Gets a valid OAuth2 access token, refreshing if necessary
        
        :return: A valid access token
        :raises Exception: If token acquisition fails
        """
        if self.is_token_valid():
            return self.access_token
        return self.refresh_token()

    def is_token_valid(self):
        """
        Checks if the current token is valid and not expired
        
        :return: True if the token is valid, false otherwise
        """
        return self.access_token and self.expires_at and time.time() < self.expires_at

    def refresh_token(self):
        """
        Refreshes the OAuth2 access token using client credentials grant
        
        :return: The new access token
        :raises Exception: If token refresh fails
        """
        try:
            request_data = {
                'grant_type': self.config.get_grant_type(),
                'client_id': self.config.get_credential_id(),
                'client_secret': self.config.get_credential_secret(),
                'scope': self.config.get_scope()
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.post(
                self.config.get_cognito_endpoint(),
                data=request_data,
                headers=headers
            )
            if response.status_code != 200:
                raise Exception("OAuth2 token request failed with status {}: {}".format(response.status_code, response.text))

            data = response.json()
            
            if 'access_token' not in data:
                raise Exception('No access token received from OAuth2 endpoint')

            self.access_token = data['access_token']
            # Set expiration time with a 30-second buffer to avoid edge cases
            expires_in = data.get('expires_in', 3600)  # Default to 1 hour if not provided
            expires_in_with_buffer = expires_in - 30
            self.expires_at = time.time() + expires_in_with_buffer
            
            return self.access_token
            
        except requests.exceptions.RequestException as e:
            # Clear existing token on failure
            self.clear_token()
            raise Exception("OAuth2 token request failed: {}".format(str(e)))
        except json.JSONDecodeError as e:
            # Clear existing token on failure
            self.clear_token()
            raise Exception("Failed to parse OAuth2 token response: {}".format(str(e)))
        except Exception as e:
            # Clear existing token on failure
            self.clear_token()
            raise e

    def clear_token(self):
        """
        Clears the cached token, forcing a refresh on the next get_token() call
        """
        self.access_token = None
        self.expires_at = None
