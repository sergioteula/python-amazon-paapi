import secrets

from amazon_paapi import AmazonApi

amazon = AmazonApi(
    secrets.KEY, secrets.SECRET, secrets.TAG, secrets.COUNTRY, throttling=2
)


print("\nGet items")
print("=========================================================")
product = amazon.get_items("B01N5IB20Q")
print(product[0].item_info.title.display_value)


print("Search items")
print("=========================================================")
items = amazon.search_items(keywords="nintendo", item_count=3)
for item in items.items:
    print(item.item_info.title.display_value)


print("\nGet variations")
print("=========================================================")
items = amazon.get_variations("B08F63PPNV", variation_count=3)
for item in items.items:
    print(item.item_info.title.display_value)


print("\nGet nodes")
print("=========================================================")
items = amazon.get_browse_nodes(["667049031"])  # Only available in spanish marketplace
for item in items:
    print(item.display_name)
