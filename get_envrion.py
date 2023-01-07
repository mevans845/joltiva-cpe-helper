import os
from dotenv import load_dotenv

load_dotenv()


def get_env(key):
    """
    Get the value of an environment variable
    :param key: environment variable name
    :return: environment variable value
    """
    return os.environ.get(key)
