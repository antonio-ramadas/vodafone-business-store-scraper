import re

import validators
import logging
from scrapy.exceptions import DropItem


class ProductValidator:
    """
    Stateless validator able to be an `Item Pipeline component
    <https://docs.scrapy.org/en/2.1/topics/item-pipeline.html>`_ on Scrappy.

    This class validates a given item of :py:class:`src.domain.product.Product` with a series of validators.

    Invalid items are dropped. Valid items are returned to go further down the line.
    """

    __logger = logging.getLogger(__name__)

    def valid_name(self, item):
        """
        Validates the name of a given item of :py:class:`src.domain.product.Product`.

        Checks the name is not empty.

        :param item: Product to be validated.
        :return: True if product passed validation, False otherwise.
        """
        if item['name']:
            ProductValidator.__logger.debug('Product has valid name: %s', item)
            return True

        ProductValidator.__logger.warning('Product contains invalid name: %s', item)
        return False

    def valid_price(self, item):
        """
        Validates the price of a given item of :py:class:`src.domain.product.Product`.

        Currency (€ or $ or £) or  may or may not exist as first or last character.
        Amount can have decimal precision separated either by dot or comma (also optional).

        Valid formats:
         - 1
         - 1.2345
         - €1.2345
         - €1,2345
         - €1,2345€ # this verification is somewhat dummy and this would be valid
         - £1.2345
         - $1.2345

        :param item: Product to be validated.
        :return: True if product passed validation, False otherwise.
        """
        if re.match(r'^[€£$]?\d+([.,])?\d*[€£$]?$', item['price']) is not None:
            ProductValidator.__logger.debug('Product has valid price: %s', item)
            return True

        ProductValidator.__logger.warning('Product contains invalid price: %s', item)
        return False

    def valid_url(self, item):
        """
        Validates the url of a given item of :py:class:`src.domain.product.Product`.

        URL validation is performed according to :py:func:`validators.url.url`.

        :param item: Product to be validated.
        :return: True if product passed validation, False otherwise.
        """
        if validators.url(item['url']) is True:
            ProductValidator.__logger.debug('Product has valid URL: %s', item)
            return True

        ProductValidator.__logger.warning('Product contains invalid URL: %s', item)
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
            ProductValidator.__logger.debug('Valid Product: %s', item)
            return item

        ProductValidator.__logger.warning('Invalid Product: %s', item)
        raise DropItem('Invalid Product: %s' % item)
