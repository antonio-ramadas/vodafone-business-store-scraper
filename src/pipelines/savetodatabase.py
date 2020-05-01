import logging

from scrapy.exceptions import DropItem

from src.databases.databasefactory import DatabaseFactory
from src.environmentvariables import EnvironmentVariables


class SaveToDatabase:
    """
    Database storing class able to be an `Item Pipeline component
    <https://docs.scrapy.org/en/2.1/topics/item-pipeline.html>`_ on Scrappy.

    This class inserts new :py:class:`src.domain.product.Product` on the database and drops existent ones.

    Database is instantiated according to :py:class:`src.databases.databasefactory.DatabaseFactory`.
    """
    __logger = logging.getLogger(__name__)

    def __init__(self, database_url):
        """
        Stores the database URL.

        :param database_url: URL of the database to connect to.
        """
        self.database_url = database_url

    @classmethod
    def from_crawler(cls, crawler):
        """
        Retrieves the necessary arguments to initialize this Item Component.

        The single required configured parameter is `src.environmentvariables.EnvironmentVariables.DATABASE_URL_ARG`.

        :param crawler: Used to choose the appropriate database.
        :return: :py:class:`src.pipelines.savetodatabase.SaveToDatabase` instance.
        """
        return cls(crawler.settings.get(EnvironmentVariables.DATABASE_URL_ARG))

    def open_spider(self, spider):
        """
        Instantiates database connection.

        Check :py:class:`src.databases.databasefactory.DatabaseFactory` initialization details.

        :param spider: Unused.
        """
        self.db = DatabaseFactory.get_database(self.database_url)

    def close_spider(self, spider):
        """
        Closes the database connection.
        :param spider: Unused.
        """
        self.db.close()

    def process_item(self, item, spider):
        """
        Inserts the given item of :py:class:`src.domain.product.Product` in the database. If it already exists, then it
        is dropped. Otherwise, the item is returned for further processing.

        :param item: Product to be inserted.
        :param spider: Unused.
        :return: item if new, :py:class:`scrapy.exceptions.DropItem` is thrown otherwise.
        """
        is_new_item = self.db.insert(item)

        if is_new_item:
            SaveToDatabase.__logger.debug('Inserted new product on the database: %s', item)
            return item
        else:
            SaveToDatabase.__logger.info('Product already exists on the database: %s', item)
            raise DropItem('Product already exists on the database: %s' % item)
