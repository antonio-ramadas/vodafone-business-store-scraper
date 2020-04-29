from abc import abstractmethod


class Notifier:
    """
    Abstract class representing a notifier.

    A notifier publishes the given information to the configured end.
    """

    @abstractmethod
    def new_product(self, product):
        """
        Synchronously notifies about a new product.

        :param product: :py:class:`src.domain.product.Product`.
        """
        pass

    @abstractmethod
    def error(self, msg):
        """
        Synchronously notifies about an error.

        :param msg: Error to be published.
        """
        pass
