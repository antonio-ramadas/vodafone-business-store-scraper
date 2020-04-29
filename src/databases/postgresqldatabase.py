import logging

import psycopg2

from src.databases.database import Database


class PostgreSqlDatabase(Database):
    __logger = logging.getLogger(__name__)

    def __init__(self, database_url):
        super().__init__()
        try:
            self.connection = psycopg2.connect(database_url, sslmode='require')
            self.connection.autocommit = False
            self.cursor = self.connection.cursor()
        except Exception as exception:
            if self.connection:
                self.close()

            PostgreSqlDatabase.__logger.error("Could not connect to database! url='%s' exception='%s'",
                                              database_url, exception)
            raise exception

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
        query_parameters = {
            'name': product['name'],
            'price': product['price'],
            'url': product['url']
        }

        self.cursor.execute('SELECT EXISTS(SELECT 1 from vodafone.products WHERE name=%(name)s);', query_parameters)

        did_the_product_already_exist = self.cursor.fetchone()[0]

        self.cursor.execute('''
            INSERT INTO vodafone.products (name, price, url) VALUES (%(name)s, %(price)s, %(url)s)
                ON CONFLICT (name) DO UPDATE SET price=%(price)s;
        ''', query_parameters)

        self.connection.commit()

        return not did_the_product_already_exist

    def close(self):
        self.cursor.close()
        self.connection.close()
