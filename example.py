from amazon_paapi import AmazonApi
import secrets


amazon = AmazonApi(secrets.KEY, secrets.SECRET, secrets.TAG, secrets.COUNTRY)
product = amazon.get_product('B01N5IB20Q')
print(product.title)
