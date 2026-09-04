"""OAuth2 settings shared by the synchronous and the asynchronous clients."""

from __future__ import annotations

from amazon_creatorsapi.errors import InvalidArgumentError

# Scopes and grant type accepted by the auth endpoints of Amazon
COGNITO_SCOPE = "creatorsapi/default"
LWA_SCOPE = "creatorsapi::default"
GRANT_TYPE = "client_credentials"

# Seconds subtracted from the lifetime of a token, so it is refreshed before
# the actual expiration
TOKEN_EXPIRATION_BUFFER = 30

# Lifetime assumed for a token when the auth endpoint does not send one
DEFAULT_EXPIRATION = 3600

# Auth flow of every family of versions, keyed by the major number of the
# version. The family decides the scope, how the token request is encoded and
# whether the version travels in the Authorization header, so a version of an
# unknown family cannot be used by pointing the library to another endpoint:
# it needs the flow of its family added here.
COGNITO_FLOW = "cognito"
LWA_FLOW = "lwa"
FAMILY_FLOWS = {"2": COGNITO_FLOW, "3": LWA_FLOW}

# Auth endpoint of every version of the API, Cognito for 2.x and LWA for 3.x
VERSION_ENDPOINTS = {
    "2.1": "https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token",
    "2.2": "https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token",
    "2.3": "https://creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token",
    "3.1": "https://api.amazon.com/auth/o2/token",
    "3.2": "https://api.amazon.co.uk/auth/o2/token",
    "3.3": "https://api.amazon.co.jp/auth/o2/token",
}


def get_flow(version: str) -> str | None:
    """Return the auth flow that a version authenticates with.

    Args:
        version: API version in use.

    Returns:
        The flow of the family of the version, or None when the library does
        not know how to authenticate that family.

    """
    # A version given as a number is turned into text instead of failing, as
    # the value is reported back in the error of an unsupported version
    major = str(version).partition(".")[0]
    return FAMILY_FLOWS.get(major)


def is_lwa(version: str) -> bool:
    """Return whether a version authenticates with Login with Amazon.

    Args:
        version: API version in use.

    Returns:
        True for the versions using LWA, False for the ones using Cognito.

    """
    return get_flow(version) == LWA_FLOW


def get_scope(version: str) -> str:
    """Return the OAuth2 scope of a version.

    Args:
        version: API version in use.

    Returns:
        The scope to ask the auth endpoint for.

    """
    return LWA_SCOPE if is_lwa(version) else COGNITO_SCOPE


def build_authorization_header(version: str, token: str) -> str:
    """Return the Authorization header that a version expects.

    Args:
        version: API version in use.
        token: OAuth2 access token of the request.

    Returns:
        The value of the Authorization header, which carries the version of
        the credentials in the Cognito flow and only the token in the LWA one.

    """
    if is_lwa(version):
        return f"Bearer {token}"
    return f"Bearer {token}, Version {version}"


def get_auth_endpoint(version: str, auth_endpoint: str | None = None) -> str:
    """Return the auth endpoint to use, validating the version when needed.

    Args:
        version: API version in use.
        auth_endpoint: Endpoint provided by the user, which takes precedence
            over the one of the version and makes valid any version of a
            family that the library knows how to authenticate.

    Returns:
        The URL used to get the OAuth2 token.

    Raises:
        InvalidArgumentError: If the family of the version is unknown, or if
            the version is not in the list and no endpoint is given.

    """
    endpoint = auth_endpoint.strip() if auth_endpoint else ""

    if version in VERSION_ENDPOINTS:
        return endpoint or VERSION_ENDPOINTS[version]

    # A custom endpoint is not enough for an unknown family, as the flow of a
    # new one is not known: the request would be sent with the encoding, the
    # scope and the headers of Cognito, which Amazon rejects without saying why
    if get_flow(version) is None:
        families = ", ".join(f"{family}.x" for family in FAMILY_FLOWS)
        msg = (
            f"Unsupported version: {version}. The library only knows how to "
            f"authenticate the {families} versions, so a newer one needs "
            f"support added to the library and not just a custom auth_endpoint"
        )
        raise InvalidArgumentError(msg)

    if not endpoint:
        supported = ", ".join(VERSION_ENDPOINTS)
        msg = (
            f"Unsupported version: {version}. Supported versions are: "
            f"{supported}. A newer version of a known family can be used by "
            f"providing its auth_endpoint"
        )
        raise InvalidArgumentError(msg)

    return endpoint
