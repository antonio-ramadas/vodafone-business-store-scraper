import logging

import validators
from scrapy.exceptions import DropItem

from src.notifiers.notifierfactory import NotifierFactory


class ProductValidator:
    """
    Stateless validator able to be an `Item Pipeline component
    <https://docs.scrapy.org/en/2.1/topics/item-pipeline.html>`_ on Scrappy.

    This class validates a given item of :py:class:`src.domain.product.Product` with a series of validators.

    Invalid items are dropped. Valid items are returned to go further down the line.
    """

    __logger = logging.getLogger(__name__)

    def __init__(self, crawler_settings):
        """
        Stores crawler_settings.

        :param crawler_settings: Settings of the crawler :py:class:`scrapy.settings.Settings`.
        """
        self.crawler_settings = crawler_settings

    @classmethod
    def from_crawler(cls, crawler):
        """
        Retrieves the necessary arguments to initialize this Item Component.

        Mainly the crawler settings to get the appropriate notifier.

        :param crawler: Used to choose the appropriate notifier.
        :return: :py:class:`src.pipelines.productvalidator.ProductValidator` instance.
        """
        return cls(crawler.settings)

    def open_spider(self, spider):
        """
        Instantiates the notifier.

        Check :py:class:`src.notifiers.notifierfactory.NotifierFactory` initialization details.

        :param spider: Unused.
        """
        self.notifier = NotifierFactory.get_notifier(self.crawler_settings)

    def valid_name(self, item):
        """
        Validates the name of a given item of :py:class:`src.domain.product.Product`.

        Checks the name is not empty.

        :param item: Product to be validated.
        :return: True if product passed validation, False otherwise.
        """
        if item['name']:
            ProductValidator.__logger.debug("Product has valid name: '%s'", item)
            return True

        ProductValidator.__logger.warning("Product contains invalid name: '%s'", item)
        return False

    def valid_price(self, item):
        """
        Validates the price of a given item of :py:class:`src.domain.product.Product`.

        Only valid if it is non-negative.

        :param item: Product to be validated.
        :return: True if product passed validation, False otherwise.
        """
        if item['price'] >= 0:
            ProductValidator.__logger.debug("Product has valid price: '%s'", item)
            return True

        ProductValidator.__logger.warning("Product contains invalid price: '%s'", item)
        return False

    def valid_url(self, item):
        """
        Validates the url of a given item of :py:class:`src.domain.product.Product`.

        URL validation is performed according to :py:func:`validators.url.url`.

        :param item: Product to be validated.
        :return: True if product passed validation, False otherwise.
        """
        if validators.url(item['url']) is True:
            ProductValidator.__logger.debug("Product has valid URL: '%s'", item)
            return True

        ProductValidator.__logger.warning("Product contains invalid URL: '%s'", item)
        return False

    def process_item(self, item, spider):
        """
        Validates a given item of :py:class:`src.domain.product.Product` by checking the name, price and URL.

        Invalid items are dropped.

        :param item: Product to be validated.
        :param spider: Unused.
        :return: item if valid, :py:class:`scrapy.exceptions.DropItem` is thrown otherwise.
        """
        if self.valid_name(item) and self.valid_price(item) and self.valid_url(item):
            ProductValidator.__logger.debug("Valid Product: '%s'", item)
            return item

        ProductValidator.__logger.warning("Invalid Product: '%s'", item)
        self.notifier.warning("Invalid Product: '%s'" % item)
        raise DropItem("Invalid Product: '%s'" % item)
