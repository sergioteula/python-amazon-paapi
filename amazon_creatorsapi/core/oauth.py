"""OAuth2 settings shared by the synchronous and the asynchronous clients."""

from __future__ import annotations

# Scopes and grant type accepted by the auth endpoints of Amazon
COGNITO_SCOPE = "creatorsapi/default"
LWA_SCOPE = "creatorsapi::default"
GRANT_TYPE = "client_credentials"

# Seconds subtracted from the lifetime of a token, so it is refreshed before
# the actual expiration
TOKEN_EXPIRATION_BUFFER = 30

# Lifetime assumed for a token when the auth endpoint does not send one
DEFAULT_EXPIRATION = 3600

# Auth endpoint of every version of the API, Cognito for 2.x and LWA for 3.x
VERSION_ENDPOINTS = {
    "2.1": "https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token",
    "2.2": "https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token",
    "2.3": "https://creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token",
    "3.1": "https://api.amazon.com/auth/o2/token",
    "3.2": "https://api.amazon.co.uk/auth/o2/token",
    "3.3": "https://api.amazon.co.jp/auth/o2/token",
}


def is_lwa(version: str) -> bool:
    """Return whether a version authenticates with Login with Amazon.

    Args:
        version: API version in use.

    Returns:
        True for the versions using LWA, False for the ones using Cognito.

    """
    return version.startswith("3.")


def get_scope(version: str) -> str:
    """Return the OAuth2 scope of a version.

    Args:
        version: API version in use.

    Returns:
        The scope to ask the auth endpoint for.

    """
    return LWA_SCOPE if is_lwa(version) else COGNITO_SCOPE


def get_auth_endpoint(version: str, auth_endpoint: str | None = None) -> str:
    """Return the auth endpoint to use, validating the version when needed.

    Args:
        version: API version in use.
        auth_endpoint: Endpoint provided by the user, which takes precedence
            over the one of the version and makes any version valid.

    Returns:
        The URL used to get the OAuth2 token.

    Raises:
        ValueError: If the version is not supported and no endpoint is given.

    """
    if auth_endpoint and auth_endpoint.strip():
        return auth_endpoint

    if version not in VERSION_ENDPOINTS:
        supported = ", ".join(VERSION_ENDPOINTS)
        msg = f"Unsupported version: {version}. Supported versions are: {supported}"
        raise ValueError(msg)

    return VERSION_ENDPOINTS[version]
