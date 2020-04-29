from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from src.environmentvariables import EnvironmentVariables
from src.spiders.vodafonebusinessstore import VodafoneBusinessStore

if __name__ == '__main__':
    settings = Settings()

    settings.set(EnvironmentVariables.DATABASE_URL_ARG, EnvironmentVariables.DATABASE_URL)

    settings.set('ITEM_PIPELINES', {
        'src.pipelines.productvalidator.ProductValidator': 100,
        'src.pipelines.duplicatesfilter.DuplicatesFilter': 200,
        'src.pipelines.savetodatabase.SaveToDatabase': 300,
        # 'src.pipelines.notifier.Notifier': 400
    })

    process = CrawlerProcess(settings)
    process.crawl(VodafoneBusinessStore)
    process.start()
