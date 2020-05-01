import logging

from src.environmentvariables import EnvironmentVariables
from src.notifiers.slacknotifier import SlackNotifier


class NotifierFactory:
    """
    https://en.wikipedia.org/wiki/Abstract_factory_pattern
    """
    __logger = logging.getLogger(__name__)

    __notifiers = {
        'slack': None
    }

    @staticmethod
    def get_notifier(crawler_settings):
        """
        Instantiates a notifier from the specified notifier according to necessary settings.

        Throws :py:class:`builtins.ValueError` if notifier is not configured.

        The reason to pass the whole blob of settings is that different notifiers may require different arguments to be
        initialised.

        If the requested notifier has already been instantiated, then it it returned.

        :param crawler_settings: :py:class:`scrapy.settings.Settings` of the :py:class:`scrapy.crawler.Crawler`.
        :return: Concrete instance of :py:class:`src.notifiers.notifier.Notifier`.
        """

        notifier = crawler_settings.get(EnvironmentVariables.NOTIFIER_ARG)

        if notifier not in NotifierFactory.__notifiers:
            NotifierFactory.__logger.error(
                "Invalid notifier requested! Got '%s', but should be one listed at the Notifiers Enum!", notifier)
            raise ValueError(
                "Invalid notifier requested! Got '%s', but should be one listed at the Notifiers Enum" % notifier)

        if NotifierFactory.__notifiers.get(notifier) is not None:
            return NotifierFactory.__notifiers.get(notifier)

        notifier_instance = None

        if notifier == 'slack':
            notifier_instance = SlackNotifier(
                token=crawler_settings.get(EnvironmentVariables.SLACK_TOKEN_ARG),
                channel=crawler_settings.get(EnvironmentVariables.SLACK_CHANNEL_ARG))
        else:
            NotifierFactory.__logger.error("Unimplemented notifier found! notifier='%s'", notifier)
            raise ValueError("Unimplemented notifier found! notifier='%s'" % notifier)

        NotifierFactory.__notifiers[notifier] = notifier_instance

        return notifier_instance
