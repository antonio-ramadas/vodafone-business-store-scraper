from scrapy.exceptions import DropItem


class DuplicatesFilter:
    def __init__(self):
        self.products_seen = set()

    def process_item(self, item, spider):
        if item['name'] in self.products_seen:
            raise DropItem("Duplicate product found: %s" % item)
        else:
            self.products_seen.add(item['name'])
            return item
