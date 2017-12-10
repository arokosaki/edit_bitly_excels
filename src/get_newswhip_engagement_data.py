import requests,json,time
from collections import namedtuple
from .api_key import API_KEY
from .exceptions import NewswhipError,OutOfRequests,APIKeyExpired,RUN_OUT_MESSAGE,API_EXPIRED_MESSAGE
from .log_and_interface import LogMessages,http_log_setup



log = http_log_setup()

class SendApiPostRequest(object):

    API_URL = 'https://api.newswhip.com/v1/'
    HEADERS = {'Content-Type': 'application/json',}
    DAY_IN_SECONDS = 86400
    TIME_LIMIT_DAYS = 182


    def __init__(self,api_key=None,headers=None):

        self.api_key = api_key or API_KEY
        self.params = (('key', self.api_key),)
        self.headers = headers or self.HEADERS

    @classmethod
    def get_max_from(cls):
        '''

        :return: the max time from which newswhip saves data
        '''
        now = time.time()
        return round((now - cls.DAY_IN_SECONDS * cls.TIME_LIMIT_DAYS) * 1000)

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
        :exception: NewsWhipError and sub classes OutOfRequests and ApiKeyExpired
        '''

        url = self.API_URL + request_type
        data = self._create_data_string(filters=filters,**kwargs)
        log.debug('sending request')
        api_request = requests.post(url=url,
                                    headers=self.headers,
                                    params=self.params,
                                    data=data)

        log.debug(LogMessages.REQUEST_LOG_MESSAGE.format(api_request.request.url, api_request.request.body))
        log.debug(LogMessages.RESPONSE_LOG_MESSAGE.format(api_request.status_code,''))

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




class GetFacebookStats(SendApiPostRequest):

    FILTER_BASE_STRING = r'external_link:\"{}\"'


    def __init__(self):
        self.result = namedtuple('fb_stats',
                                 ['comments','likes','shares','loves','wows','hahas','sads',
                                  'angrys','total_engagement_count'])

        super(GetFacebookStats,self).__init__()

    def fix_url(self,url):
        return url.replace('_','/posts/')

    def get_fb_stats(self,url):
        From = self.get_max_from()
        filters = self.FILTER_BASE_STRING.format(self.fix_url(url))
        while True:
            try:
                response = self.send_api_request(request_type='fbPosts',
                                                 filters=filters,
                                                 sort_by="fb_likes",
                                                 From=From)
                break
            except OutOfRequests:
                pass

        if response['fbPosts']:
            reactions = response['fbPosts'][0]['fb_data']['reactions']
            return self.result(comments=reactions['comments'],
                               likes=reactions['likes'],
                               shares=reactions['shares'],
                               loves=reactions['loves'],
                               wows=reactions['wows'],
                               hahas=reactions['hahas'],
                               sads=reactions['sads'],
                               angrys=reactions['angrys'],
                               total_engagement_count=response['fbPosts'][0]['fb_data']['total_engagement_count'])
        else:
            return self.result(comments='Null',
                               likes='Null',
                               shares='Null',
                               loves='Null',
                               wows='Null',
                               hahas='Null',
                               sads='Null',
                               angrys='Null',
                               total_engagement_count='Null')