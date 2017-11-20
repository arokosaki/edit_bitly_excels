from .get_newswhip_engagement_data import GetEngagmentStats,OutOfRequests,NewswhipError
from .get_full_url import GetFullURL
from .exceptions import InternetException
from .log_and_interface import printProgressBar
import logging
from collections import namedtuple

class EditFile(object):


    NEW_HEADLINES = ['Full URL', 'Facebook Total', 'Twitter', 'Total Engagement']

    def __init__(self):
        self.result = namedtuple('result',['result','line_number','error'])


    def execute(self, data_list,start_from=None):
        start_from = start_from or 2
        result = []
        total = len(data_list[start_from:])
        logging.info('starting file edit')
        printProgressBar(0, total)
        result.append(data_list[0]+self.NEW_HEADLINES)
        for i,row in enumerate(data_list[start_from-1:]):
            try:
                full_url = GetFullURL().execute(row[5])
                engagement = GetEngagmentStats().get_engagement_stats_from_url(full_url)
            except (InternetException,KeyboardInterrupt) as e:
                logging.exception(e)
                print()
                return self.result(result=result,line_number=(i-1+start_from),error=e)
            row.append(full_url)
            row.append(engagement.fb_total)
            row.append(engagement.twitter)
            row.append(engagement.total_engagement)
            result.append(row)
            printProgressBar(i+1,total)
        return result

