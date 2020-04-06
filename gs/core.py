"""SoftwareShield core api"""

from .intf import *
from .util import *

import os
import logging



class Core(object):
    _inst = None # unique instance

    @classmethod
    def getInstance(cls):
        if cls._inst is None:
            cls._inst = Core()
        return cls._inst
    
    def __new__(cls):
        if cls._inst is None:
           cls._inst = object.__new__(cls)
           cls._inst._onCreate() # call once and only once!
        return cls._inst

    def _onCreate(self):
        ''' Initialize Core only once here '''
        self._rc = 0

    @staticmethod
    def getVersion():
        '''get SDK version'''
        return pchar2str(gsGetVersion())

    def init(self, productId, pathToLic, password):
        """
        Loads from local storage first, if not found, loads from external license file.
        """
        mustbe(str, "productId", productId)
        mustbe(str, "pathToLic", pathToLic)
        mustbe(str, "password", password)

        if pathToLic != '':
            pathToLic = os.path.abspath(pathToLic)
            logging.info("license path (%s)", pathToLic)

        self._rc = gsInit(str2pchar(productId), str2pchar(pathToLic), str2pchar(password),None)
        logging.debug("rc: %d", self._rc)
        return self._rc == 0

    @property
    def LastErrorCode(self):
        ''' Last SDK error code '''
        return gsGetLastErrorCode()

    