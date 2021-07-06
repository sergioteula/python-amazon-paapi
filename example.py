from amazon_paapi.paapi import AmazonAPI
import secrets


amazon = AmazonAPI(secrets.KEY, secrets.SECRET, secrets.TAG, secrets.COUNTRY)
product = amazon.get_product('B01N5IB20Q')
print(product.title)
