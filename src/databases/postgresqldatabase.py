import logging

import psycopg2

from src.databases.database import Database


class PostgreSqlDatabase(Database):
    __logger = logging.getLogger(__name__)

    def __init__(self, database_url):
        super().__init__()
        try:
            self.connection = psycopg2.connect(database_url, sslmode='require')
            self.cursor = self.connection.cursor()
        except Exception as exception:
            PostgreSqlDatabase.__logger.error("Could not connect to database! url='{}' exception='{}'",
                                              database_url, exception)
            raise exception
        finally:
            if self.connection:
                self.close()

        self.__init_schema()
        self.__init_table()

    def __init_schema(self):
        self.cursor.execute('CREATE SCHEMA IF NOT EXISTS vodafone;')
        self.connection.commit()
        PostgreSqlDatabase.__logger.info('Created schema')

    def __init_table(self):
        create_table = '''
        create table if not exists vodafone.products(
            id    serial not null constraint products_pk primary key,
            name  text   not null,
            price text   not null,
            url   text   not null);

        create unique index if not exists products_name_uindex on vodafone.products (name);
        '''
        self.cursor.execute(create_table)
        self.connection.commit()
        PostgreSqlDatabase.__logger.info('Created table')

    def insert(self, product):
        # TODO insert given product and see if it already existed
        pass

    def close(self):
        self.cursor.close()
        self.connection.close()
