"""Data parser for instance creation."""
import pprint

import six

class Class:
    """Base class for creating the product instance."""
    pass


class AmazonBrowseNode():
    swagger_types = {
        'ancestor': 'BrowseNodeAncestor',
        'children': 'BrowseNodeChildren',
        'context_free_name': 'str',
        'display_name': 'str',
        'id': 'str',
        'is_root': 'bool',
        'sales_rank': 'int'
    }

    def __init__(self, node):
        self.ancestor = node.ancestor
        self.children = node.children
        self.context_free_name = node.context_free_name
        self.display_name = node.display_name
        self.id = node.id
        self.is_root = node.is_root
        self.sales_rank = node.sales_rank

    def to_dict(self):
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(AmazonBrowseNode, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        return self.to_str()

    def __eq__(self, other):
        if not isinstance(other, AmazonBrowseNode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


def parse_browsenode(browse_nodes_response):
    """Parse browse node data and creates a dict.

    Args:
        browse_nodes_response (list): List of browse nodes responses.

    Returns:
        dict: Dict with browse node information.
    """
    mapped_response = {}
    for browse_node in browse_nodes_response:
        mapped_response[browse_node.id] = browse_node
    return mapped_response


def parse_product(item):
    """Parse item data and creates product instance.

    Args:
        item (instance): The instance with the data from Amazon API.

    Returns:
        instance: Product instance with parsed data.
    """
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
    try:
        product.parent_asin = item.parent_asin
    except Exception:
        product.parent_asin = None

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
        product.product.pages_count = item.item_info.content_info.pages_count.display_value
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
    product.product.dimensions.length = Class()
    try:
        product.product.dimensions.length.value = item.item_info.product_info.item_dimensions.length.display_value
    except Exception:
        product.product.dimensions.length.value = None
    try:
        product.product.dimensions.length.unit = item.item_info.product_info.item_dimensions.length.unit
    except Exception:
        product.product.dimensions.length.unit = None
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
    try:
        for x in product.images.variants.small:
            product.images.cropped.small.append(x.replace('_SL', '_AC'))
    except Exception:
        pass
    try:
        for x in product.images.variants.medium:
            product.images.cropped.medium.append(x.replace('_SL', '_AC'))
    except Exception:
        pass
    try:
        for x in product.images.variants.large:
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
    if not product.trade_in.eligible and not product.trade_in.price and not product.trade_in.currency:
        product.trade_in = None

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
