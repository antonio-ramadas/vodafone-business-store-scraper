import logging

from scrapy.exceptions import DropItem


class DuplicatesFilter:
    """
    Stateless validator able to be an `Item Pipeline component
    <https://docs.scrapy.org/en/2.1/topics/item-pipeline.html>`_ on Scrappy.

    This class removes duplicates of :py:class:`src.domain.product.Product` by dropping them.
    """
    __logger = logging.getLogger(__name__)

    def __init__(self):
        self.products_seen = set()

    def process_item(self, item, spider):
        """
        Check if the item of :py:class:`src.domain.product.Product` has been seen before by keeping track of all product
        names seen so far.

        Two :py:class:`src.domain.product.Product` are considered the same if they have the same name.

        :param item: Product to be validated.
        :param spider: Unused.
        :return:
        """
        if item['name'] in self.products_seen:
            DuplicatesFilter.__logger.info('Dropping duplicated product: %s', item)
            raise DropItem('Duplicate product found: %s' % item)
        else:
            DuplicatesFilter.__logger.info('Adding unseen product: %s', item)
            self.products_seen.add(item['name'])
            return item
