from src.notifiers.notifierfactory import NotifierFactory


class ProductNotifier:
    # TODO Document
    def __init__(self, crawler_settings):
        self.crawler_settings = crawler_settings

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.notifier = NotifierFactory.get_notifier(self.crawler_settings)

    def process_item(self, item, spider):
        self.notifier.new_product(item)
        return item
