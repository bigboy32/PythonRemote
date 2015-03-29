import logging


class Singleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


class Logger(object):
    '''Used for logging in this app'''

    __metaclass__ = Singleton

    logger = None

    def __init__(self):
        """
        Creates a logger instance and sets the relevant settings
        :rtype : None
        """
        self.logger = logging.getLogger('Remote')
        fhdlr = logging.FileHandler('remote.log')
        shdlr = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')
        fhdlr.setFormatter(formatter)
        shdlr.setFormatter(formatter)
        self.logger.addHandler(fhdlr)
        self.logger.addHandler(shdlr)
        self.logger.setLevel(logging.INFO)

    def change_log_level(self, level):
        """
        Changes the current level of statements which should be logged
        :param level: The level to begin logging at
        :type level: int
        :rtype : None
        """
        self.logger.setLevel(level)

    def info(self, msg, *args, **kwargs):
        """
        Logs a formatted message at the info level
        :rtype : None
        :param msg: The message format which should be used when logging
        :param args: An array of parameters to be placed into the format string
        :param kwargs: A named dictionary of parameters to be placed into the format string
        """
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        Logs a formatted message at the warning level
        :rtype : None
        :param msg: The message format which should be used when logging
        :param args: An array of parameters to be placed into the format string
        :param kwargs: A named dictionary of parameters to be placed into the format string
        """
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        Logs a formatted message at the error level
        :rtype : None
        :param msg: The message format which should be used when logging
        :param args: An array of parameters to be placed into the format string
        :param kwargs: A named dictionary of parameters to be placed into the format string
        """
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        Logs a formatted message at the critical level
        :rtype : None
        :param msg: The message format which should be used when logging
        :param args: An array of parameters to be placed into the format string
        :param kwargs: A named dictionary of parameters to be placed into the format string
        """
        self.logger.critical(msg, *args, **kwargs)
