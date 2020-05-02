import logging

from slack import WebClient
from slack.errors import SlackApiError

from src.notifiers.notifier import Notifier


class SlackNotifier(Notifier):
    """
    This class requires multiple permissions to the correct operation. It uses two Slack API endpoints:
     - https://api.slack.com/methods/chat.postMessage
     - https://api.slack.com/methods/conversations.list
     - https://api.slack.com/methods/conversations.create
     - https://api.slack.com/methods/conversations.join

    The permissions to post messages are mandatory to ensure a correct operation of the class.
    The permissions to list channels are mandatory to retrieve the id of the channel so this class is able to publish
    messages.
    The permissions to create channels are optional and only necessary if the channel is to be created by this class.
    The permissions to join channels are optional and only necessary if the channel is to be joined by this class.

    The Slack token passed as argument to the constructor must have the necessary scopes.
    """
    __logger = logging.getLogger(__name__)

    def __init__(self, token, channel):
        """
        Initialises the Slack client and, if necessary, creates the channel.

        Failing to create the channel does not prevent the correct operation of the instance.

        If a channel already exists, it won't be unarchived.

        After confirming the existence of the channel, it will be retrieved the channel's id.
        With this id, the bot will join the Slack channel.

        :param token: Slack token to the workspace.
        :param channel: Slack channel's name where the messages will be sent.
        """
        self.client = WebClient(token=token)
        self.channel = channel

        self.__connect_to_channel(channel)

    def __connect_to_channel(self, channel):
        try:
            self.client.conversations_create(name=channel)
            SlackNotifier.__logger.info("Created Slack channel '%s'.", channel)
            self.__set_channel_id(channel)
        except SlackApiError as e:
            SlackNotifier.__logger.warning(
                "Failed to create channel '%s' due to '%s'. You can ignore this warning if the channel already exists. "
                "Attempting to join channel.", channel, e.response['error'])
            self.__join_channel(channel)

    def __join_channel(self, channel):
        self.__set_channel_id(channel)
        try:
            self.client.conversations_join(channel=self.channel_id)
            SlackNotifier.__logger.info("Joined Slack channel '%s'.", channel)
        except SlackApiError as e:
            if e.response['error'] == 'is_archived':
                SlackNotifier.__logger.error("Requested channel '%s' is archived. Slack bot cannot post messages there."
                                             " Please unarchive it or choose another channel.", channel)
                raise ValueError("Requested channel '%s' is archived. Slack bot cannot post messages there. "
                                 "Please unarchive it or choose another channel." % channel)

            SlackNotifier.__logger.warning(
                "Failed to join channel '%s' due to '%s'. You can ignore this warning if the bot has already joined.",
                channel, e.response['error'])

    def __set_channel_id(self, channel):
        public_channels = []

        try:
            public_channels = self.client.conversations_list().get('channels')
            SlackNotifier.__logger.debug("Retrieved the following list of channels: '%s'", public_channels)
        except SlackApiError as e:
            SlackNotifier.__logger.error(
                "Failed to retrieve list of Slack channels to find the id of '%s'. error='%s'", channel, e)
            raise ValueError(
                "Failed to retrieve list of Slack channels to find the id of '%s'. error='%s'" % (channel, e))

        channel_ids = [public_channel for public_channel in public_channels if public_channel['name'] == channel]

        # Most likely the channel was not found or Slack now supports multiple channels with the same name
        if len(channel_ids) != 1:
            SlackNotifier.__logger.error(
                "Channel '%s' not found. Have you spelled the channel's name correctly? Are you sure it is public?",
                channel)
            raise ValueError(
                "Channel '%s' not found. Have you spelled the channel's name correctly? Are you sure it is public?" %
                channel)

        self.channel_id = channel_ids[0]['id']
        SlackNotifier.__logger.info("Found id '%s' for the Slack channel '%s'.", self.channel_id, self.channel)

    def new_product(self, product):
        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                text=":new: <%s|%s> is now available at %s" % (product['url'], product['name'], product['price']))
            SlackNotifier.__logger.debug("New product posted on Slack. product='%s'", product)
        except SlackApiError as e:
            SlackNotifier.__logger.error(
                "Failed to notify a new product to Slack! error='%s' product='%s'", e.response['error'], product)

    def warning(self, msg):
        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                text=":warning: Something happened that may required your attention.\n```%s```" % msg)
            SlackNotifier.__logger.debug("Error message posted on Slack. msg='%s'", msg)
        except SlackApiError as e:
            SlackNotifier.__logger.error(
                "Failed to publish an error to Slack! error_response='%s' error_msg='%s'", e.response['error'], msg)

    def error(self, msg):
        try:
            self.client.chat_postMessage(
                channel=self.channel_id,
                text=":rotating_light: An error occurred!\n```%s```" % msg)
            SlackNotifier.__logger.debug("Error message posted on Slack. msg='%s'", msg)
        except SlackApiError as e:
            SlackNotifier.__logger.error(
                "Failed to publish an error to Slack! error_response='%s' error_msg='%s'", e.response['error'], msg)
