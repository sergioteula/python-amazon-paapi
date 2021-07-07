from amazon_paapi.sdk.models import condition, merchant
from amazon_paapi import AmazonApi
import secrets
from amazon_paapi.models import Condition

amazon = AmazonApi(secrets.KEY, secrets.SECRET, secrets.TAG, secrets.COUNTRY)
product = amazon.get_items('B01N5IB20Q', condition=Condition.NEW)
print(product[0].item_info.title.display_value)
