
import logging


class Logger:
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s] - %(message)s', datefmt='%d/%b/%Y %H:%M:%S'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt, datefmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        th = logging.handlers.TimedRotatingFileHandler(
            filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        sh.setFormatter(format_str)
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


my_log = Logger('my_log.log')
