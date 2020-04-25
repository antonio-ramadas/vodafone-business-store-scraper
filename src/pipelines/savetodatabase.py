import scrapy


class SaveToDatabasePipeline(scrapy.Spider):
    name = 'drop_existent_products_pipeline'

    # TODO connect to DB and drop existent elements
    def process_item(self, item, spider):
        # print(item)
        # raise DropItem("Product already exists: '{}'".format(item.get('name')))
        return item
