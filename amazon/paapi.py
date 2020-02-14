"""Amazon Product Advertising API 5.0 wrapper for Python"""

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.condition import Condition
from paapi5_python_sdk.get_items_request import GetItemsRequest
from paapi5_python_sdk.get_items_resource import GetItemsResource
from paapi5_python_sdk.partner_type import PartnerType
import time
import logging


REGIONS = {
    'AU': 'us-west-2',
    'BR': 'us-east-1',
    'CA': 'us-east-1',
    'FR': 'eu-west-1',
    'DE': 'eu-west-1',
    'IN': 'eu-west-1',
    'IT': 'eu-west-1',
    'JP': 'us-west-2',
    'MX': 'us-east-1',
    'ES': 'eu-west-1',
    'TR': 'eu-west-1',
    'AE': 'eu-west-1',
    'UK': 'eu-west-1',
    'US': 'us-east-1'
}
DOMAINS = {
    'AU': 'com.au',
    'BR': 'com.br',
    'CA': 'ca',
    'FR': 'fr',
    'DE': 'de',
    'IN': 'in',
    'IT': 'it',
    'JP': 'co.jp',
    'MX': 'com.mx',
    'ES': 'es',
    'TR': 'com.tr',
    'AE': 'ae',
    'UK': 'co.uk',
    'US': 'com'
}


class Product:
    pass


def get_asin(url):
    """Find the ASIN from a given URL.

    Args:
        url (string): The URL containing the product ASIN.

    Returns:
        string: Product ASIN. None if ASIN not found.
    """
    split_url = url.split('?')[0].replace('?', '/').replace('&', '/').split('/')
    for c in list(reversed(split_url)):
        if len(c) == 10 and c.isalnum():
            return c


class AmazonAPI:
    """Creates an instance containing your API credentials.

    Args:
        key (string): Your API key.
        secret (string): Your API secret.
        tag (string): The tag you want to use for the URL.
        country (string): Country code.
        throttling (float, optional): Reduce this value to wait longer between API calls.
    """
    def __init__(self, key, secret, tag, country, throttling=0.9):
        self.key = key
        self.secret = secret
        self.tag = tag
        self.throttling = throttling
        self.country = country
        self.host = 'webservices.amazon.' + DOMAINS[country]
        self.region = REGIONS[country]
        self.marketplace = 'www.amazon.' + DOMAINS[country]
        self.last_query_time = time.time()

    def get_product(self, product_id, condition=Condition.NEW):
        """Find product information for a specific product on Amazon.

        Args:
            product_id (string): Product ASIN or URL. You can send multiple products separated
                by commas.
            condition (class, optional): Specify the product condition. Defaults to NEW.

        Returns:
            class instance: An instance of the class Product containing all the available
                information when only 1 product is returned.
            list of class instances: A list containing 1 instance of the class Product for
                each returned product.
        """
        api = DefaultApi(access_key=self.key,
                         secret_key=self.secret,
                         host=self.host,
                         region=self.region)

        product_id = product_id.split(',')
        asin_list = []
        for x in product_id:
            asin_list.append(get_asin(x.strip()))

        product_resources = [
            GetItemsResource.BROWSENODEINFO_BROWSENODES,
            GetItemsResource.BROWSENODEINFO_BROWSENODES_ANCESTOR,
            GetItemsResource.BROWSENODEINFO_BROWSENODES_SALESRANK,
            GetItemsResource.BROWSENODEINFO_WEBSITESALESRANK,
            GetItemsResource.IMAGES_PRIMARY_SMALL,
            GetItemsResource.IMAGES_PRIMARY_MEDIUM,
            GetItemsResource.IMAGES_PRIMARY_LARGE,
            GetItemsResource.IMAGES_VARIANTS_SMALL,
            GetItemsResource.IMAGES_VARIANTS_MEDIUM,
            GetItemsResource.IMAGES_VARIANTS_LARGE,
            GetItemsResource.ITEMINFO_BYLINEINFO,
            GetItemsResource.ITEMINFO_CONTENTINFO,
            GetItemsResource.ITEMINFO_CONTENTRATING,
            GetItemsResource.ITEMINFO_CLASSIFICATIONS,
            GetItemsResource.ITEMINFO_EXTERNALIDS,
            GetItemsResource.ITEMINFO_FEATURES,
            GetItemsResource.ITEMINFO_MANUFACTUREINFO,
            GetItemsResource.ITEMINFO_PRODUCTINFO,
            GetItemsResource.ITEMINFO_TECHNICALINFO,
            GetItemsResource.ITEMINFO_TITLE,
            GetItemsResource.ITEMINFO_TRADEININFO,
            GetItemsResource.OFFERS_LISTINGS_AVAILABILITY_MAXORDERQUANTITY,
            GetItemsResource.OFFERS_LISTINGS_AVAILABILITY_MESSAGE,
            GetItemsResource.OFFERS_LISTINGS_AVAILABILITY_MINORDERQUANTITY,
            GetItemsResource.OFFERS_LISTINGS_AVAILABILITY_TYPE,
            GetItemsResource.OFFERS_LISTINGS_CONDITION,
            GetItemsResource.OFFERS_LISTINGS_CONDITION_SUBCONDITION,
            GetItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
            GetItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
            GetItemsResource.OFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
            GetItemsResource.OFFERS_LISTINGS_DELIVERYINFO_SHIPPINGCHARGES,
            GetItemsResource.OFFERS_LISTINGS_ISBUYBOXWINNER,
            GetItemsResource.OFFERS_LISTINGS_LOYALTYPOINTS_POINTS,
            GetItemsResource.OFFERS_LISTINGS_MERCHANTINFO,
            GetItemsResource.OFFERS_LISTINGS_PRICE,
            GetItemsResource.OFFERS_LISTINGS_PROGRAMELIGIBILITY_ISPRIMEEXCLUSIVE,
            GetItemsResource.OFFERS_LISTINGS_PROGRAMELIGIBILITY_ISPRIMEPANTRY,
            GetItemsResource.OFFERS_LISTINGS_PROMOTIONS,
            GetItemsResource.OFFERS_LISTINGS_SAVINGBASIS,
            GetItemsResource.OFFERS_SUMMARIES_HIGHESTPRICE,
            GetItemsResource.OFFERS_SUMMARIES_LOWESTPRICE,
            GetItemsResource.OFFERS_SUMMARIES_OFFERCOUNT,
            GetItemsResource.PARENTASIN,
            GetItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MAXORDERQUANTITY,
            GetItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MESSAGE,
            GetItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_MINORDERQUANTITY,
            GetItemsResource.RENTALOFFERS_LISTINGS_AVAILABILITY_TYPE,
            GetItemsResource.RENTALOFFERS_LISTINGS_BASEPRICE,
            GetItemsResource.RENTALOFFERS_LISTINGS_CONDITION,
            GetItemsResource.RENTALOFFERS_LISTINGS_CONDITION_SUBCONDITION,
            GetItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISAMAZONFULFILLED,
            GetItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISFREESHIPPINGELIGIBLE,
            GetItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_ISPRIMEELIGIBLE,
            GetItemsResource.RENTALOFFERS_LISTINGS_DELIVERYINFO_SHIPPINGCHARGES,
            GetItemsResource.RENTALOFFERS_LISTINGS_MERCHANTINFO]

        try:
            request = GetItemsRequest(partner_tag=self.tag,
                                      partner_type=PartnerType.ASSOCIATES,
                                      marketplace=self.marketplace,
                                      condition=condition,
                                      item_ids=asin_list,
                                      resources=product_resources)
        except ValueError as exception:
            logging.error('Error in forming GetItemsRequest: %s' % (exception))
            return

        try:
            """Wait before doing the request"""
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            """Request to the API"""
            response = api.get_items(request)

            """Parse the response and create a product"""
            if response.items_result is not None:
                if len(response.items_result.items) > 0:
                    results = []
                    for item in response.items_result.items:
                        product = Product()
                        product.asin = item.asin

                        try:
                            product.url = item.detail_page_url
                        except Exception:
                            product.url = None

                        """Parse ItemInfo data"""
                        try:
                            item_info = item.item_info
                        except Exception:
                            item_info = None
                        try:
                            product.title = item_info.title.display_value
                        except Exception:
                            product.title = None
                        try:
                            product.release_date = item_info.product_info.release_date.display_value
                        except Exception:
                            product.release_date = None
                        try:
                            product.features = item_info.features.display_values
                        except Exception:
                            product.features = None
                        try:
                            product.category = item_info.classifications.product_group.display_value
                        except Exception:
                            product.category = None
                        try:
                            product.subcategory = item_info.classifications.binding.display_value
                        except Exception:
                            product.subcategory = None
                        try:
                            product.brand = item_info.by_line_info.brand.display_value
                        except Exception:
                            product.brand = None
                        try:
                            product.manufacturer = item_info.by_line_info.manufacturer.display_value
                        except Exception:
                            product.manufacturer = None

                        """Parse Images data"""
                        try:
                            images = item.images
                        except Exception:
                            images = None
                        try:
                            product.image_large = images.primary.large.url.replace('.jpg',
                                                                                   '._AC_.jpg')
                        except Exception:
                            product.image_large = None
                        try:
                            product.image_medium = images.primary.medium.url.replace('_SL', '_AC')
                        except Exception:
                            product.image_medium = None
                        try:
                            product.image_small = images.primary.small.url.replace('_SL', '_AC')
                        except Exception:
                            product.image_small = None
                        try:
                            product.image_variants = []
                            for variant in images.variants:
                                try:
                                    product.image_variants.append(
                                        variant.large.url.replace('.jpg', '._AC_.jpg'))
                                except Exception:
                                    pass
                            if not product.image_variants:
                                product.image_variants = None
                        except Exception:
                            product.image_variants = None

                        """Parse Offers Listings data"""
                        product.prices = Product()
                        try:
                            listings = item.offers.listings[0]
                        except Exception:
                            listings = None
                        try:
                            product.prices.availability = listings.availability.message
                        except Exception:
                            product.prices.availability = None
                        try:
                            product.prices.price = listings.price.amount
                        except Exception:
                            product.prices.price = None
                        try:
                            product.prices.pvp = listings.saving_basis.amount
                        except Exception:
                            product.prices.pvp = None
                        try:
                            product.prices.currency = listings.price.currency
                        except Exception:
                            product.prices.currency = None

                        """Parse Offers Summaries data"""
                        product.offers = Product()
                        try:
                            product.offers = item.offers.summaries
                        except Exception:
                            product.offers = None

                        results.append(product)
                    if len(results) == 0:
                        return None
                    elif len(results) == 1:
                        return results[0]
                    else:
                        return results
                else:
                    return None

        except Exception as exception:
            logging.error(str(exception))
            return None
