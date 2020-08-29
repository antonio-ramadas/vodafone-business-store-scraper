import logging

from src.notifiers.notifier import Notifier


class LogNotifier(Notifier):
    __logger = logging.getLogger(__name__)

    def new_product(self, product):
        LogNotifier.__logger.info("New product notification. product='%s'", product)

    def warning(self, msg):
        LogNotifier.__logger.warning("Something happened that may required your attention.\n%s", msg)

    def error(self, msg):
        LogNotifier.__logger.error("An error occurred.\n%s", msg)
