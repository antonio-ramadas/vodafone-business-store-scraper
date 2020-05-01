import logging

from scrapy.exceptions import DropItem

from src.notifiers.notifierfactory import NotifierFactory


class DuplicatesFilter:
    """
    Stateless filter able to be an `Item Pipeline component
    <https://docs.scrapy.org/en/2.1/topics/item-pipeline.html>`_ on Scrappy.

    This class removes duplicates of :py:class:`src.domain.product.Product` by dropping them.
    """
    __logger = logging.getLogger(__name__)

    def __init__(self, crawler_settings):
        """
        Stores crawler_settings and start with the no products seen.

        :param crawler_settings: Settings of the crawler :py:class:`scrapy.settings.Settings`.
        """
        self.crawler_settings = crawler_settings
        self.products_seen = set()

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
            DuplicatesFilter.__logger.info("Dropping duplicated product: '%s'", item)
            self.notifier.warning("Dropping duplicated product: '%s'" % item)
            raise DropItem("Duplicate product found: '%s'" % item)
        else:
            DuplicatesFilter.__logger.info("Adding unseen product: '%s'", item)
            self.products_seen.add(item['name'])
            return item
