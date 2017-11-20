import re
import requests


class GetFullURL(object):

    RE_STRING = r'http://bit\.ly/\w+'

    def extract_url(self, string):
        '''

        :param str string:
        :return str: bitly url
        '''
        bitly_url_re = re.compile(self.RE_STRING)
        return bitly_url_re.search(string)

    def get_full_url(self,bitly_url):
        '''

        :param str bitly_url:
        :return str: full url
        '''
        res = requests.get(bitly_url)
        return res.url

    def execute(self,string):
        bitly_url = self.extract_url(string).group()
        return self.get_full_url(bitly_url)
