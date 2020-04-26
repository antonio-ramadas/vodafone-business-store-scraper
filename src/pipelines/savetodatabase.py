import os

import psycopg2


class SaveToDatabase:
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    # TODO connect to DB and drop existent elements
    def process_item(self, item, spider):
        # print(item)
        # raise DropItem("Product already exists: '{}'".format(item.get('name')))
        return item
