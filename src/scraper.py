from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from src.pipelines.savetodatabase import SaveToDatabasePipeline

if __name__ == '__main__':
    settings = Settings()
    settings.set('ITEM_PIPELINES', {
        'src.pipelines.savetodatabase.SaveToDatabasePipeline': 100
    })

    process = CrawlerProcess(settings)
    process.crawl(SaveToDatabasePipeline)
    process.start()
