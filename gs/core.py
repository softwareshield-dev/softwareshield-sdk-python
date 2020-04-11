"""SoftwareShield core api"""

from .intf import *
from .util import *
from .entity import *
from .var import Variable

import os
import logging

# decorator to enforce the gs.Core must be initialized before api can be called.
def core_must_inited(f):
    def new_f(*args):
        if not Core._inst._inited:
            raise Exception("gs.Core must be initialized!")
        return f(*args)
    return new_f

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
        self._rc = -1 # not initialized
        self._inited = False # not initialized yet
        self._entities = None # entity list

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

        # already initialized successfully?
        if self._rc != 0:
            if pathToLic != '':
                pathToLic = os.path.abspath(pathToLic)
                logging.info(f"license path ({pathToLic})")

            self._rc = gsInit(str2pchar(productId), str2pchar(pathToLic), str2pchar(password),None)
            self._inited = True
            logging.debug(f"rc: {self._rc}")
        else:
            logging.debug("init: already initialized, bypass")
        
        return self._rc == 0

    def cleanUp(self):
        """
        Cleanup sdk resources on app exit.
        """
        gsCleanUp()

    @property
    @core_must_inited
    def lastErrorCode(self):
        ''' Last SDK error code '''
        return gsGetLastErrorCode()

    @property
    @core_must_inited
    def lastErrorMessage(self):
        ''' Last SDK error message '''
        return pchar2str(gsGetLastErrorMessage())


    @property
    @core_must_inited
    def productId(self):
        ''' Product Id '''
        return pchar2str(gsGetProductId())
    
    @property
    @core_must_inited
    def productName(self):
        ''' Product Name '''
        return pchar2str(gsGetProductName())
    
    @property
    @core_must_inited
    def buildId(self):
        ''' License Build Id '''
        return gsGetBuildId()

    @property
    @core_must_inited
    def entities(self):
        ''' all defined entities '''
        if not self._entities:
            self._entities = [ Entity(gsOpenEntityByIndex(i)) for i in range(gsGetEntityCount()) ]
        return self._entities
    
    @core_must_inited
    def getEntityById(self, entityId):
        ''' get entity by its id'''
        for e in self.entities:
            if e.id == entityId:
                return e

        msg = f"entity not found, id=({entityId})"
        logging.warning(msg)
        raise ValueError(msg)

    @core_must_inited
    def getVariable(self, name):
        h = gsGetVariable(str2pchar(name))
        if h is None:
            raise ValueError(f"variable ({name}) not found")

        return Variable(h)
