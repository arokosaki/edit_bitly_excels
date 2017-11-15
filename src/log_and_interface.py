import logging


def printProgressBar (iteration, total, prefix = 'Progress',
                      suffix = 'Complete', decimals = 1, length = 50, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + ' ' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

def http_log_setup():

    http_log = logging.FileHandler('http-api.log')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    http_log.setFormatter(formatter)
    http_log.setLevel(logging.DEBUG)
    log = logging.getLogger('http_log')
    log.addHandler(http_log)
    log.setLevel(logging.DEBUG)
    return log

def main_log_setup():

    main_log = logging.FileHandler('main.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    main_log.setFormatter(formatter)
    main_log.setLevel(logging.INFO)
    log = logging.getLogger()
    log.addHandler(main_log)
    log.setLevel(logging.DEBUG)
    return log

class LogMessages(object):

    REQUEST_LOG_MESSAGE ='Request URL: {}\n' + '\t' * 6 + '  Request body: {}'
    RESPONSE_LOG_MESSAGE = 'Response Code: {}\n' + '\t' * 6 + '  Response body: {}'
