import logging

from slack import WebClient
from slack.errors import SlackApiError

from src.notifiers.notifier import Notifier


class SlackNotifier(Notifier):
    """
    This class requires multiple permissions to the correct operation. It uses two Slack API endpoints:
     - https://api.slack.com/methods/chat.postMessage
     - https://api.slack.com/methods/conversations.create

    The permissions to post messages are mandatory to ensure a correct operation of the class.
    The permissions to create channels are optional and only necessary if the channel is created by this class.

    The Slack token passed as argument to the constructor must have the necessary scopes.
    """
    __logger = logging.getLogger(__name__)

    def __init__(self, token, channel):
        """
        Initialises the Slack client and, if necessary, creates the channel.

        Failing to create the channel does not prevent the correct operation of the instance.

        If a channel already exists, it won't be unarchived.

        :param token: Slack token to the workspace.
        :param channel: Slack channel where the messages will be sent.
        """
        self.client = WebClient(token=token)
        self.channel = channel

        self.__create_channel(channel)

    def __create_channel(self, channel):
        try:
            self.client.conversations_create(name=channel)
        except SlackApiError as e:
            SlackNotifier.__logger.warning(
                "Failed to create channel '%s' due to '%s'. You can ignore this warning if the channel already exists.",
                channel, e.response['error'])

        SlackNotifier.__logger.info('Channel created.')

    def new_product(self, product):
        try:
            self.client.chat_postMessage(
                channel=self.channel,
                text=":new: <%s|%s> is now available at %s" % (product['url'], product['name'], product['price']))
        except SlackApiError as e:
            SlackNotifier.__logger.error(
                "Failed to notify a new product to Slack! error='%s' product='%s'", e.response['error'], product)

    def error(self, msg):
        try:
            self.client.chat_postMessage(
                channel=self.channel,
                text=":rotating_light: An error occurred! error='%s'" % msg)
        except SlackApiError as e:
            SlackNotifier.__logger.error(
                "Failed to publish an error to Slack! error_response='%s' error_msg='%s'", e.response['error'], msg)
