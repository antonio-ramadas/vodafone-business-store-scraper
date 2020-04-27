import os


class EnvironmentVariables:
    """
    Static class that holds all the available environment variables that are accessed by the program.
    """
    DATABASE_URL_ARG = 'DATABASE_URL'
    DATABASE_URL = os.environ[DATABASE_URL_ARG]
