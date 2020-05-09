import scrapy


class Product(scrapy.Item):
    """
    Domain representation of a Product with name, price and URL.
    """

    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()

    def __str__(self):
        return super.__str__(self).replace('\n', '')
