from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from src.environmentvariables import EnvironmentVariables
from src.spiders.vodafonebusinessstore import VodafoneBusinessStore


class Scraper:
    """
    Functional class that contains a single method.
    """
    @staticmethod
    def scrape():
        """
        Scrapes the Vodafone Business Store. For each scrapped product, it validates it, check it was already processed,
         saves to a database and notifies about it.
        """
        settings = Settings()

        settings.set(EnvironmentVariables.DATABASE_URL_ARG, EnvironmentVariables.DATABASE_URL)

        settings.set(EnvironmentVariables.NOTIFIER_ARG, EnvironmentVariables.NOTIFIER)
        settings.set(EnvironmentVariables.SLACK_TOKEN_ARG, EnvironmentVariables.SLACK_TOKEN)
        settings.set(EnvironmentVariables.SLACK_CHANNEL_ARG, EnvironmentVariables.SLACK_CHANNEL)

        settings.set('ITEM_PIPELINES', {
            'src.pipelines.productvalidator.ProductValidator': 100,
            'src.pipelines.duplicatesfilter.DuplicatesFilter': 200,
            'src.pipelines.savetodatabase.SaveToDatabase': 300,
            'src.pipelines.productnotifier.ProductNotifier': 400
        })

        settings.set('TELNETCONSOLE_ENABLED', False)

        process = CrawlerProcess(settings)
        process.crawl(VodafoneBusinessStore)
        process.start()


if __name__ == '__main__':
    Scraper.scrape()
