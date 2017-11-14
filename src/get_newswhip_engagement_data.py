import requests,json,time
from collections import namedtuple
from .api_key import API_KEY
from .exceptions import NewswhipError,OutOfRequests,APIKeyExpired,RUN_OUT_MESSAGE,API_EXPIRED_MESSAGE
from .log_and_interface import LogMessages,http_log_setup
import logging



log = http_log_setup()

class SendApiPostRequest(object):

    API_URL = 'https://api.newswhip.com/v1/'
    HEADERS = {'Content-Type': 'application/json',}


    def __init__(self,api_key=None,headers=None):

        self.api_key = api_key or API_KEY
        self.params = (('key', self.api_key),)
        self.headers = headers or self.HEADERS

    @classmethod
    def _cast_param_into_string(cls, param_info):
        '''

        :param param_info: the value of the parameter
        :return: the value in appropriate string form
        '''

        if type(param_info) == str:
            return '"%s"' % (param_info)
        if type(param_info) == bool:
            return '%s' % (str(param_info).lower())
        if type(param_info) == int:
            return '%s' % param_info
        if type(param_info) == list:
            for i,entry in enumerate(param_info):
                param_info[i] = cls._cast_param_into_string(entry)
            return '%s' % param_info
        else:
            raise ValueError

    @classmethod
    def _create_data_string(cls, filters, **kwargs):
        '''

        :param str filters:
        :param kwargs:
        :return: data of api request in json format string
        :rtype str
        '''
        # add filters string
        result = r'{"filters": ["%s"]' % filters

        # add additional params to query
        if kwargs:
            for key in kwargs:
                value = cls._cast_param_into_string(kwargs[key])
                result += ', "%s": %s' % (key.lower(),value)

        result += '}'

        return result

    def send_api_request(self,request_type,filters,**kwargs):
        '''
        this function sends NewsWhip api post commands and returns answer as python list[dict]

        :param str request_type: the type of api request being sent.
                                 list of options can be found at http://docs.newswhip.com/?shell#post-requests
        :param str filters: every api request requires a filter.
                            more info at http://docs.newswhip.com/?shell#post-v1-articles
        :param kwargs: additional params that can be added to request.
                       list of options and their defaults can be found here:
                       http://docs.newswhip.com/?shell#post-v1-articles under Query Parameters
                       'from' parameter should be written with capital F to avoid confusion with python key word

        :return: information list[dict]
        :rtype: list[dict]
        '''

        url = self.API_URL + request_type
        data = self._create_data_string(filters=filters,**kwargs)
        log.debug('sending request')
        api_request = requests.post(url=url,
                                    headers=self.headers,
                                    params=self.params,
                                    data=data)

        log.debug(LogMessages.REQUEST_LOG_MESSAGE.format(api_request.request.url, api_request.request.body))
        log.debug(LogMessages.RESPONSE_LOG_MESSAGE.format(api_request.status_code, api_request.text))

        response = json.loads(api_request.text)

        # find api error
        if type(response) == dict and 'error' in response.keys():
            identifier = response['error']['id']
            message = response['error']['message']
            if message == RUN_OUT_MESSAGE:
                raise OutOfRequests(identifier=identifier,messege=message)
            elif message == API_EXPIRED_MESSAGE:
                raise APIKeyExpired(identifier=identifier,messege=message)
            else:
                raise NewswhipError(identifier=identifier,messege=message)
        else:
            return response





class GetEngagmentStats(object):

    DAY_IN_SECONDS = 86400
    TIME_LIMIT_DAYS = 182
    FILTERS_BASE_STRING = r"href:\"%s\""

    def __init__(self,api_key=None,api=None):

        self.engagement_stats = namedtuple('engagement_stats', ['fb_total', 'twitter', 'total_engagement'])
        self.api = api or SendApiPostRequest(api_key)


    @classmethod
    def _get_max_from(cls):
        now = time.time()
        return round((now - cls.DAY_IN_SECONDS * cls.TIME_LIMIT_DAYS) * 1000)

    def get_engagement_stats_from_url(self,url):
        max_from = self._get_max_from()
        filters = self.FILTERS_BASE_STRING % url
        while True:
            try:
                response = self.api.send_api_request(request_type='stats',
                                                     filters=filters,
                                                     sort_by='fb_total.sum',
                                                     aggregate_by='domain',
                                                     From=max_from)
                break
            except OutOfRequests:
                logging.warning('out of api requests')
                pass

        if response:
            return self.engagement_stats(fb_total=response[0]['stats']['fb_total']['sum'],
                                         twitter=response[0]['stats']['twitter']['sum'],
                                         total_engagement=response[0]['total'])
        else:
            return self.engagement_stats('Null','Null','Null')
