from urllib.error import URLError
from requests.exceptions import ConnectionError,RequestException

class NewswhipError(Exception):

    def __init__(self, identifier, messege):
        super(NewswhipError, self).__init__(messege)
        self.id = identifier

class OutOfRequests(NewswhipError):
    """when your 100 request every 5 minutes runs out"""

class APIKeyExpired(NewswhipError):
    """api key has expired"""


class NotFBPost(ValueError):
    """not a known fb post url"""

NoInternet = ConnectionError
InternetException = RequestException


RUNNING_ERROR_STRING = 'Execution has stopped in the middle do to exception: \'{}\'\n' \
                       'last line to be processed is: {}.'

RUN_OUT_MESSAGE = r'Youâ€™re requesting too many kittens! Slow down!'
API_EXPIRED_MESSAGE = r'Your API has expired. Please contact api@newswhip.com to renew it.'
