import logging

from src.databases.postgresqldatabase import PostgreSqlDatabase


class DatabaseFactory:
    """
    https://en.wikipedia.org/wiki/Abstract_factory_pattern
    """
    __logger = logging.getLogger(__name__)

    __vendors = {
        'postgres': PostgreSqlDatabase
    }

    @staticmethod
    def get_database(database_url):
        """
        Instantiates a database connection from the vendor specified from the given url.

        Throws :py:class:`builtins.ValueError` if vendor is not configured.

        :param database_url: URL to database.
        :return: Concrete instance of :py:class:`src.databases.database.Database`.
        """
        vendor = database_url[:database_url.find(':')]

        if vendor in DatabaseFactory.__vendors:
            DatabaseFactory.__logger.info("Retrieving database for vendor '%s'", vendor)
            return DatabaseFactory.__vendors[vendor](database_url)
        else:
            DatabaseFactory.__logger.error("Requested vendor is not supported! vendor='%s' database_url='%s'",
                                           vendor, database_url)
            supported_vendors = ','.join(DatabaseFactory.__vendors.keys())
            raise ValueError(
                "Invalid vendor requested! Got '%s' but should be one of '%s'" % (vendor, supported_vendors))
