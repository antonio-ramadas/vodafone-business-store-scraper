from src.notifiers.notifierfactory import NotifierFactory


class ProductNotifier:
    """
    Notifier class able to be an `Item Pipeline component
    <https://docs.scrapy.org/en/2.1/topics/item-pipeline.html>`_ on Scrappy.

    This class notifies about every :py:class:`src.domain.product.Product` and returns it for further processing.
    """

    def __init__(self, crawler_settings):
        """
        Stores the crawler settings.

        :param crawler_settings: Settings of the crawler :py:class:`scrapy.settings.Settings`.
        """
        self.crawler_settings = crawler_settings

    @classmethod
    def from_crawler(cls, crawler):
        """
        Retrieves the necessary arguments to initialize this Item Component.

        Mainly the crawler settings to get the appropriate notifier.

        :param crawler: Used to choose the appropriate notifier.
        :return: :py:class:`src.pipelines.productnotifier.ProductNotifier` instance.
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
        Uses the appropriate notifier to publish about the product.

        :param item: Product to be advertised.
        :param spider: Unused
        :return: item
        """
        self.notifier.new_product(item)
        return item
