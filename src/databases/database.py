from abc import abstractmethod


class Database:
    """
    Abstract class representing a database.
    """

    @abstractmethod
    def __init__(self):
        """
        Connects to database and initializes the schema, if necessary.
        """
        pass

    @abstractmethod
    def insert(self, product):
        """
        Inserts atomically the given product in the database only if it does not exist.

        :param product: :py:class:`src.domain.product.Product` to be inserted.
        :return: True if product was inserted, False if product already exists.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Closes the database connection.
        """
        pass
