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


NoInternet = ConnectionError
InternetException = RequestException


RUNNING_ERROR_STRING = 'Execution has stopped in the middle do to exception: \'{}\'\n' \
                       'Excepction text: \'{}\'\nlast line to be processed is: {}.'
