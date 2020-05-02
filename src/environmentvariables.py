import os


class EnvironmentVariables:
    """
    Static class that holds all the available environment variables that are accessed by the program.
    """
    PORT_ARG = 'PORT'
    PORT = os.getenv(PORT_ARG)

    DATABASE_URL_ARG = 'DATABASE_URL'
    DATABASE_URL = os.getenv(DATABASE_URL_ARG)

    NOTIFIER_ARG = 'NOTIFIER'
    NOTIFIER = os.getenv(NOTIFIER_ARG)

    SLACK_TOKEN_ARG = 'SLACK_TOKEN'
    SLACK_TOKEN = os.getenv(SLACK_TOKEN_ARG)

    SLACK_CHANNEL_ARG = 'SLACK_CHANNEL'
    SLACK_CHANNEL = os.getenv(SLACK_CHANNEL_ARG)
