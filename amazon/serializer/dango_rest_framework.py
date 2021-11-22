from rest_framework import serializers


class _AmazonValueUnitSerializer(serializers.Serializer):
    value = serializers.FloatField()
    unit = serializers.CharField()


class _AmazonDimensionsSerializer(serializers.Serializer):
    height = _AmazonValueUnitSerializer()
    length = _AmazonValueUnitSerializer()
    width = _AmazonValueUnitSerializer()


class _AmazonProductSerializer(serializers.Serializer):
    features = serializers.ListField()
    languages = serializers.ListField()
    formats = serializers.ListField()
    pages_count = serializers.ListField()
    color = serializers.CharField()
    unit_count = serializers.IntegerField()
    size = serializers.CharField()
    dimensions = _AmazonDimensionsSerializer()
    weight = _AmazonValueUnitSerializer()


class _AmazonContributorsSerializer(serializers.Serializer):
    name = serializers.CharField()
    role = serializers.CharField()


class _AmazonExternalIdsSerializer(serializers.Serializer):
    ean = serializers.ListField()
    isbn = serializers.ListField()
    upc = serializers.ListField()


class _AmazonInfoSerializer(serializers.Serializer):
    contributors = _AmazonContributorsSerializer(many=True)
    manufacturer = serializers.CharField()
    brand = serializers.CharField()
    model = serializers.CharField()
    part_number = serializers.CharField()
    product_group = serializers.CharField()
    binding = serializers.CharField()
    is_adult = serializers.BooleanField()
    audience_rating = serializers.CharField()
    edition = serializers.CharField()
    warranty = serializers.CharField()
    publication_date = serializers.CharField()
    release_date = serializers.CharField()
    external_ids = _AmazonExternalIdsSerializer()


class _AmazonImageVariantsSerializer(serializers.Serializer):
    small = serializers.ListField()
    medium = serializers.ListField()
    large = serializers.ListField()


class _AmazonImagesSerializer(serializers.Serializer):
    small = serializers.CharField()
    medium = serializers.CharField()
    large = serializers.CharField()
    cropped = _AmazonImageVariantsSerializer()
    variants = _AmazonImageVariantsSerializer()


class _AmazonTradeInSerializer(serializers.Serializer):
    elegible = serializers.BooleanField()
    price = serializers.FloatField()
    currency = serializers.CharField()


class _AmazonSavingsSerializer(serializers.Serializer):
    value = serializers.FloatField()
    currency = serializers.CharField()
    per_unit = serializers.FloatField()
    display = serializers.CharField()
    percentage = serializers.FloatField()


class _AmazonPriceSerializer(serializers.Serializer):
    value = serializers.FloatField()
    currency = serializers.CharField()
    per_unit = serializers.FloatField()
    display = serializers.CharField()
    savings = _AmazonSavingsSerializer()


class _AmazonPvpSerializer(serializers.Serializer):
    value = serializers.FloatField()
    currency = serializers.CharField()
    per_unit = serializers.FloatField()
    display = serializers.CharField()


class _AmazonAvailabilitySerializer(serializers.Serializer):
    max_order_quantity = serializers.IntegerField()
    min_order_quantity = serializers.IntegerField()
    type = serializers.CharField()
    message = serializers.CharField()


class _AmazonConditionSerializer(serializers.Serializer):
    condition = serializers.CharField()
    condition_display = serializers.CharField()
    sub_condition = serializers.CharField()
    sub_condition_display = serializers.CharField()


class _AmazonMerchantSerializer(serializers.Serializer):
    default_shipping_country = serializers.CharField()
    merchant_id = serializers.CharField()
    name = serializers.CharField()


class _AmazonOtherSerializer(serializers.Serializer):
    buybox_winner = serializers.BooleanField()
    loyalty_points = serializers.IntegerField()
    amazon_fulfilled = serializers.BooleanField()
    free_shipping_eligible = serializers.BooleanField()
    prime_eligible = serializers.BooleanField()
    prime_exclusive = serializers.BooleanField()
    prime_pantry = serializers.BooleanField()
    violates_map = serializers.BooleanField()
    offer_id = serializers.CharField()


class _AmazonPricesSerializer(serializers.Serializer):
    price = _AmazonPriceSerializer()
    pvp = _AmazonPvpSerializer()
    availability = _AmazonAvailabilitySerializer()
    condition = _AmazonConditionSerializer()
    merchant = _AmazonMerchantSerializer()
    other = _AmazonOtherSerializer()


class _AmazonOffersSummarySerializer(serializers.Serializer):
    highest_price = _AmazonPvpSerializer()
    lowest_price = _AmazonPvpSerializer()
    condition = _AmazonConditionSerializer()
    offer_count = serializers.IntegerField()


class AmazonProductSerializer(serializers.Serializer):
    asin = serializers.CharField(max_length=10)
    parent_asin = serializers.CharField(max_length=10)
    title = serializers.CharField()
    url = serializers.CharField()
    product = _AmazonProductSerializer()
    info = _AmazonInfoSerializer()
    images = _AmazonImagesSerializer()
    trade_in = _AmazonTradeInSerializer()
    prices = _AmazonPricesSerializer()
    offers_summary = _AmazonOffersSummarySerializer(many=True)
