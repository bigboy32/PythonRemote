import platform
import logging


class Singleton(type):
    _instances = {}
    
    def __call__(self,*args,**kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton,self).__call__(*args,**kwargs)
        return self._instances[self]
    

class Logger(object):
    '''Used for logging in this app'''
    
    __metaclass__ = Singleton
    
    logger = None
    
    def __init__(self):
        self.logger = logging.getLogger('Remote')
        fhdlr = logging.FileHandler('remote.log')
        shdlr = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')
        fhdlr.setFormatter(formatter)
        shdlr.setFormatter(formatter)
        self.logger.addHandler(fhdlr)
        self.logger.addHandler(shdlr)
        self.logger.setLevel(logging.INFO)

    def changeLogLevel(self, level):
        self.logger.setLevel(level)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg,*args,**kwargs)
        
    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg,*args,**kwargs)
        
    def error(self, msg, *args, **kwargs):
        self.logger.error(msg,*args,**kwargs)
        
    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg,*args,**kwargs)
    

    