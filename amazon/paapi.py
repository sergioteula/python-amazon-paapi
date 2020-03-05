"""Amazon Product Advertising API 5.0 wrapper for Python"""

from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.condition import Condition
from paapi5_python_sdk.get_items_request import GetItemsRequest
from paapi5_python_sdk.get_items_resource import GetItemsResource
from paapi5_python_sdk.partner_type import PartnerType
import time
import logging
import re


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


class Class:
    """Base class for creating the product instance."""


def get_asin(url):
    """Find the ASIN from a given URL.

    Args:
        url (string): The URL containing the product ASIN.

    Returns:
        string: Product ASIN. None if ASIN not found.
    """
    if re.search("^[A-Z0-9]{10}$", url):
        return url
    # since asin is alphanumeric and 10 digit
    have_asin = re.search(r"(dp|gp/product)/([a-zA-Z0-9]{10})", url)
    return have_asin.group(2) if have_asin else None


def parse_product(item):
    product = Class()
    product.raw_info = item

    # Main
    product.asin = item.asin
    try:
        product.url = item.detail_page_url
    except Exception:
        product.url = None
    try:
        product.title = item.item_info.title.display_value
    except Exception:
        product.title = None

    # Info
    product.info = Class()
    try:
        product.info.contributors = []
        for x in item.item_info.by_line_info.contributors:
            contributor = Class()
            contributor.name = x.name
            contributor.role = x.role
            product.info.contributors.append(contributor)
    except Exception:
        product.info.contributors = None
    try:
        product.info.manufacturer = item.item_info.by_line_info.manufacturer.display_value
    except Exception:
        product.info.manufacturer = None
    try:
        product.info.brand = item.item_info.by_line_info.brand.display_value
    except Exception:
        product.info.brand = None
    try:
        product.info.product_group = item.item_info.classifications.product_group.display_value
    except Exception:
        product.info.product_group = None
    try:
        product.info.binding = item.item_info.classifications.binding.display_value
    except Exception:
        product.info.binding = None
    try:
        product.info.is_adult = item.item_info.product_info.is_adult_product.display_value
    except Exception:
        product.info.is_adult = None
    try:
        product.info.edition = item.item_info.content_info.edition.display_value
    except Exception:
        product.info.edition = None
    try:
        product.info.warranty = item.item_info.manufacture_info.warranty.display_value
    except Exception:
        product.info.warranty = None
    try:
        product.info.audience_rating = item.item_info.content_rating.audience_rating.display_value
    except Exception:
        product.info.audience_rating = None
    try:
        product.info.part_number = item.item_info.manufacture_info.item_part_number.display_value
    except Exception:
        product.info.part_number = None
    try:
        product.info.model = item.item_info.manufacture_info.model.display_value
    except Exception:
        product.info.model = None
    try:
        product.info.publication_date = item.item_info.content_info.publication_date.display_value
    except Exception:
        product.info.publication_date = None
    try:
        product.info.release_date = item.item_info.product_info.release_date.display_value
    except Exception:
        product.info.release_date = None
    product.info.external_ids = Class()
    try:
        product.info.external_ids.ean = item.item_info.external_ids.ea_ns.display_values
    except Exception:
        product.info.external_ids.ean = None
    try:
        product.info.external_ids.isbn = item.item_info.external_ids.isb_ns.display_values
    except Exception:
        product.info.external_ids.isbn = None
    try:
        product.info.external_ids.upc = item.item_info.external_ids.up_cs.display_values
    except Exception:
        product.info.external_ids.upc = None

    # Product
    product.product = Class()
    try:
        product.product.features = item.item_info.features.display_values
    except Exception:
        product.product.features = None
    try:
        product.product.languages = []
        for x in item.item_info.content_info.languages.display_values:
            product.product.languages.append(x.display_value + ' ' + x.type)
    except Exception:
        product.product.languages = None
    try:
        product.product.pages_count = item.item_info.content_info.pages_count.display_values
    except Exception:
        product.product.pages_count = None
    try:
        product.product.formats = item.item_info.technical_info.formats.display_values
    except Exception:
        product.product.formats = None
    try:
        product.product.color = item.item_info.product_info.color.display_value
    except Exception:
        product.product.color = None
    try:
        product.product.unit_count = item.item_info.product_info.unit_count.display_value
    except Exception:
        product.product.unit_count = None
    product.product.dimensions = Class()
    try:
        product.product.size = item.item_info.product_info.size.display_value
    except Exception:
        product.product.size = None
    product.product.dimensions.height = Class()
    try:
        product.product.dimensions.height.value = item.item_info.product_info.item_dimensions.height.display_value
    except Exception:
        product.product.dimensions.height.value = None
    try:
        product.product.dimensions.height.unit = item.item_info.product_info.item_dimensions.height.unit
    except Exception:
        product.product.dimensions.height.unit = None
    product.product.dimensions.lenght = Class()
    try:
        product.product.dimensions.lenght.value = item.item_info.product_info.item_dimensions.lenght.display_value
    except Exception:
        product.product.dimensions.lenght.value = None
    try:
        product.product.dimensions.lenght.unit = item.item_info.product_info.item_dimensions.lenght.unit
    except Exception:
        product.product.dimensions.lenght.unit = None
    product.product.dimensions.width = Class()
    try:
        product.product.dimensions.width.value = item.item_info.product_info.item_dimensions.width.display_value
    except Exception:
        product.product.dimensions.width.value = None
    try:
        product.product.dimensions.width.unit = item.item_info.product_info.item_dimensions.width.unit
    except Exception:
        product.product.dimensions.width.unit = None
    product.product.weight = Class()
    try:
        product.product.weight.value = item.item_info.product_info.item_dimensions.weight.display_value
    except Exception:
        product.product.weight.value = None
    try:
        product.product.weight.unit = item.item_info.product_info.item_dimensions.weight.unit
    except Exception:
        product.product.weight.unit = None

    # Images
    product.images = Class()
    try:
        product.images.large = item.images.primary.large.url
    except Exception:
        product.images.large = None
    try:
        product.images.medium = item.images.primary.medium.url
    except Exception:
        product.images.medium = None
    try:
        product.images.small = item.images.primary.small.url
    except Exception:
        product.images.small = None
    try:
        product.images.variants = Class()
        product.images.variants.small = []
        product.images.variants.medium = []
        product.images.variants.large = []
        for variant in item.images.variants:
            try:
                product.images.variants.large.append(variant.large.url)
                product.images.variants.medium.append(variant.medium.url)
                product.images.variants.small.append(variant.small.url)
            except Exception:
                pass
        if not product.images.variants.small and not product.images.variants.medium and not product.images.variants.large:
            product.images.variants = None
    except Exception:
        product.images.variants = None
    product.images.cropped = Class()
    product.images.cropped.small = []
    product.images.cropped.medium = []
    product.images.cropped.large = []
    try:
        product.images.cropped.small.append(product.images.small.replace('_SL', '_AC'))
    except Exception:
        pass
    try:
        product.images.cropped.medium.append(product.images.medium.replace('_SL', '_AC'))
    except Exception:
        pass
    try:
        product.images.cropped.large.append(product.images.large.replace('.jpg', '._AC_.jpg'))
    except Exception:
        pass
    for x in product.images.variants.small:
        try:
            product.images.cropped.small.append(x.replace('_SL', '_AC'))
        except Exception:
            pass
    for x in product.images.variants.medium:
        try:
            product.images.cropped.medium.append(x.replace('_SL', '_AC'))
        except Exception:
            pass
    for x in product.images.variants.large:
        try:
            product.images.cropped.large.append(x.replace('.jpg', '._AC_.jpg'))
        except Exception:
            pass

    # Trade In
    product.trade_in = Class()
    try:
        product.trade_in.eligible = item.item_info.trade_in_info.is_eligible_for_trade_in
    except Exception:
        product.trade_in.eligible = None
    try:
        product.trade_in.price = item.item_info.trade_in_info.price.amount
    except Exception:
        product.trade_in.price = None
    try:
        product.trade_in.currency = item.item_info.trade_in_info.price.currency
    except Exception:
        product.trade_in.currency = None

    # Prices
    try:
        listings = item.offers.listings[0]
    except Exception:
        listings = None
    product.prices = Class()
    product.prices.price = Class()
    try:
        product.prices.price.value = listings.price.amount
    except Exception:
        product.prices.price.value = None
    try:
        product.prices.price.currency = listings.price.currency
    except Exception:
        product.prices.price.currency = None
    try:
        product.prices.price.per_unit = listings.price.price_per_unit
    except Exception:
        product.prices.price.per_unit = None
    try:
        product.prices.price.display = listings.price.display_amount
    except Exception:
        product.prices.price.display = None
    product.prices.price.savings = Class()
    try:
        product.prices.price.savings.value = listings.price.savings.amount
    except Exception:
        product.prices.price.savings.value = None
    try:
        product.prices.price.savings.currency = listings.price.savings.currency
    except Exception:
        product.prices.price.savings.currency = None
    try:
        product.prices.price.savings.per_unit = listings.price.savings.price_per_unit
    except Exception:
        product.prices.price.savings.per_unit = None
    try:
        product.prices.price.savings.display = listings.price.savings.display_amount
    except Exception:
        product.prices.price.savings.display = None
    try:
        product.prices.price.savings.percentage = listings.price.savings.percentage
    except Exception:
        product.prices.price.savings.percentage = None
    product.prices.pvp = Class()
    try:
        product.prices.pvp.value = listings.saving_basis.amount
    except Exception:
        product.prices.pvp.value = None
    try:
        product.prices.pvp.currency = listings.saving_basis.currency
    except Exception:
        product.prices.pvp.currency = None
    try:
        product.prices.pvp.per_unit = listings.saving_basis.price_per_unit
    except Exception:
        product.prices.pvp.per_unit = None
    try:
        product.prices.pvp.display = listings.saving_basis.display_amount
    except Exception:
        product.prices.pvp.display = None
    product.prices.availability = Class()
    try:
        product.prices.availability.message = listings.availability.message
    except Exception:
        product.prices.availability.message = None
    try:
        product.prices.availability.type = listings.availability.type
    except Exception:
        product.prices.availability.type = None
    try:
        product.prices.availability.max_order_quantity = listings.availability.max_order_quantity
    except Exception:
        product.prices.availability.max_order_quantity = None
    try:
        product.prices.availability.min_order_quantity = listings.availability.min_order_quantity
    except Exception:
        product.prices.availability.min_order_quantity = None
    product.prices.condition = Class()
    try:
        product.prices.condition.condition = listings.condition.value
    except Exception:
        product.prices.condition = None
    try:
        product.prices.condition.condition_display = listings.condition.display_value
    except Exception:
        product.prices.condition_display = None
    try:
        product.prices.condition.sub_condition = listings.condition.sub_condition.value
    except Exception:
        product.prices.sub_condition = None
    try:
        product.prices.condition.sub_condition_display = listings.condition.sub_condition.display_value
    except Exception:
        product.prices.sub_condition_display = None
    product.prices.merchant = Class()
    try:
        product.prices.merchant.default_shipping_country = listings.merchant_info.default_shipping_country
    except Exception:
        product.prices.merchant.default_shipping_country = None
    try:
        product.prices.merchant.merchant_id = listings.merchant_info.id
    except Exception:
        product.prices.merchant.merchant_id = None
    try:
        product.prices.merchant.name = listings.merchant_info.name
    except Exception:
        product.prices.merchant.name = None
    product.prices.other = Class()
    try:
        product.prices.other.buybox_winner = listings.is_buy_box_winner
    except Exception:
        product.prices.other.buybox_winner = None
    try:
        product.prices.other.loyalty_points = listings.loyalty_points
    except Exception:
        product.prices.other.loyalty_points = None
    try:
        product.prices.other.amazon_fulfilled = listings.delivery_info.is_amazon_fulfilled
    except Exception:
        product.prices.other.amazon_fulfilled = None
    try:
        product.prices.other.free_shipping_eligible = listings.delivery_info.is_free_shipping_eligible
    except Exception:
        product.prices.other.free_shipping_eligible = None
    try:
        product.prices.other.prime_eligible = listings.delivery_info.is_prime_eligible
    except Exception:
        product.prices.other.prime_eligible = None
    try:
        product.prices.other.prime_exclusive = listings.program_eligibility.is_prime_exclusive
    except Exception:
        product.prices.other.prime_exclusive = None
    try:
        product.prices.other.prime_pantry = listings.program_eligibility.is_prime_pantry
    except Exception:
        product.prices.other.prime_pantry = None
    try:
        product.prices.other.violates_map = listings.violates_map
    except Exception:
        product.prices.other.violates_map = None
    try:
        product.prices.other.offer_id = listings.id
    except Exception:
        product.prices.other.offer_id = None

    # Offers Summary
    try:
        summaries = item.offers.summaries
        product.offers_summary = []
    except Exception:
        summaries = None
        product.offers_summary = None
    if summaries:
        for x in summaries:
            offer = Class()
            offer.highest_price = Class()
            offer.lowest_price = Class()
            try:
                offer.highest_price.value = x.highest_price.amount
            except Exception:
                offer.highest_price.value = None
            try:
                offer.highest_price.currency = x.highest_price.currency
            except Exception:
                offer.highest_price.currency = None
            try:
                offer.highest_price.per_unit = x.highest_price.price_per_unit
            except Exception:
                offer.highest_price.per_unit = None
            try:
                offer.highest_price.display = x.highest_price.display_amount
            except Exception:
                offer.highest_price.display = None
            try:
                offer.lowest_price.value = x.lowest_price.amount
            except Exception:
                offer.lowest_price.value = None
            try:
                offer.lowest_price.currency = x.lowest_price.currency
            except Exception:
                offer.lowest_price.currency = None
            try:
                offer.lowest_price.per_unit = x.lowest_price.price_per_unit
            except Exception:
                offer.lowest_price.per_unit = None
            try:
                offer.lowest_price.display = x.lowest_price.display_amount
            except Exception:
                offer.lowest_price.display = None
            offer.condition = Class()
            try:
                offer.condition.condition = x.condition.value
            except Exception:
                offer.condition.condition = None
            try:
                offer.condition.condition.condition_display = x.condition.display_value
            except Exception:
                offer.condition.condition_display = None
            try:
                offer.condition.condition.sub_condition = x.condition.sub_condition.value
            except Exception:
                offer.condition.sub_condition = None
            try:
                offer.condition.condition.sub_condition_display = x.condition.sub_condition.display_value
            except Exception:
                offer.condition.sub_condition_display = None
            try:
                offer.offer_count = x.offer_count
            except Exception:
                offer.offer_count = None
            product.offers_summary.append(offer)

    return product


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

    def get_products(self, product_ids: [str, list], condition=Condition.ANY):
        """Find product information for a specific product on Amazon.

        Args:
            product_ids (string): One or more ItemIds like ASIN that uniquely identify an item or product URL. (Max 10)
            Seperated by comma or as a list.
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
        
        # clean up input data into a list stripping any extra white space
        asin_or_url_list = [x.strip() for x in product_ids.split(",")] if isinstance(product_ids, str) else product_ids
        
        # extract asin if supplied input is product url and remove any duplicate asin from cleaned list
        asin_list = list(set([get_asin(x) for x in asin_or_url_list[:10]]))

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
        except Exception as exception:
            raise exception

        try:
            # Wait before doing the request
            wait_time = 1 / self.throttling - (time.time() - self.last_query_time)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_query_time = time.time()

            response = api.get_items(request)
            if response.items_result is not None:
                if len(response.items_result.items) > 0:
                    results = []
                    for item in response.items_result.items:
                        product = parse_product(item)
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
            raise exception
