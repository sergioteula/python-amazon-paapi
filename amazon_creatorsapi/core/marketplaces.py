"""Region and marketplace mappings for Amazon Creators API."""

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

    Example:
        api = AmazonCreatorsApi(..., country=Country.ES)

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


# Mapping of country code to marketplace URL
MARKETPLACES: dict[str, str] = {
    "AU": "www.amazon.com.au",
    "BE": "www.amazon.com.be",
    "BR": "www.amazon.com.br",
    "CA": "www.amazon.ca",
    "FR": "www.amazon.fr",
    "DE": "www.amazon.de",
    "IN": "www.amazon.in",
    "IT": "www.amazon.it",
    "JP": "www.amazon.co.jp",
    "MX": "www.amazon.com.mx",
    "NL": "www.amazon.nl",
    "PL": "www.amazon.pl",
    "SG": "www.amazon.sg",
    "SA": "www.amazon.sa",
    "ES": "www.amazon.es",
    "SE": "www.amazon.se",
    "TR": "www.amazon.com.tr",
    "AE": "www.amazon.ae",
    "UK": "www.amazon.co.uk",
    "US": "www.amazon.com",
}
