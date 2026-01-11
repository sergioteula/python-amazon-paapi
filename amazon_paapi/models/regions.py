"""Region and country code definitions for Amazon marketplaces."""

from __future__ import annotations

from typing import Literal

CountryCode = Literal[
    "AU",
    "BE",
    "BR",
    "CA",
    "FR",
    "DE",
    "IN",
    "IT",
    "JP",
    "MX",
    "NL",
    "PL",
    "SG",
    "SA",
    "ES",
    "SE",
    "TR",
    "AE",
    "UK",
    "US",
]


class Country:
    """Constants for supported Amazon countries.

    Use these constants when specifying the country parameter.
    Example: AmazonApi(key, secret, tag, Country.ES)
    """

    AU: CountryCode = "AU"
    BE: CountryCode = "BE"
    BR: CountryCode = "BR"
    CA: CountryCode = "CA"
    FR: CountryCode = "FR"
    DE: CountryCode = "DE"
    IN: CountryCode = "IN"
    IT: CountryCode = "IT"
    JP: CountryCode = "JP"
    MX: CountryCode = "MX"
    NL: CountryCode = "NL"
    PL: CountryCode = "PL"
    SG: CountryCode = "SG"
    SA: CountryCode = "SA"
    ES: CountryCode = "ES"
    SE: CountryCode = "SE"
    TR: CountryCode = "TR"
    AE: CountryCode = "AE"
    UK: CountryCode = "UK"
    US: CountryCode = "US"


REGIONS: dict[str, str] = {
    "AU": "us-west-2",
    "BE": "eu-west-1",
    "BR": "us-east-1",
    "CA": "us-east-1",
    "FR": "eu-west-1",
    "DE": "eu-west-1",
    "IN": "eu-west-1",
    "IT": "eu-west-1",
    "JP": "us-west-2",
    "MX": "us-east-1",
    "NL": "eu-west-1",
    "PL": "eu-west-1",
    "SG": "us-west-2",
    "SA": "eu-west-1",
    "ES": "eu-west-1",
    "SE": "eu-west-1",
    "TR": "eu-west-1",
    "AE": "eu-west-1",
    "UK": "eu-west-1",
    "US": "us-east-1",
}


DOMAINS: dict[str, str] = {
    "AU": "com.au",
    "BE": "com.be",
    "BR": "com.br",
    "CA": "ca",
    "FR": "fr",
    "DE": "de",
    "IN": "in",
    "IT": "it",
    "JP": "co.jp",
    "MX": "com.mx",
    "NL": "nl",
    "PL": "pl",
    "SG": "sg",
    "SA": "sa",
    "ES": "es",
    "SE": "se",
    "TR": "com.tr",
    "AE": "ae",
    "UK": "co.uk",
    "US": "com",
}
