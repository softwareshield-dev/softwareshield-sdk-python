"""SoftwareShield core api"""

from .intf import *
from .util import *
from .entity import *
from .var import Variable
from .req import *

import os
import logging

# decorator to enforce the gs.Core must be initialized before api can be called.
def core_must_inited(f):
    def new_f(*args):
        if not Core._inst._inited:
            raise SdkError("gs.Core must be initialized!")
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
        raise SdkError(msg)

    @core_must_inited
    def getVariable(self, name):
        h = gsGetVariable(str2pchar(name))
        if h is None:
            raise SdkError(f"variable ({name}) not found")

        return Variable(h)

    #----- Online Activation ----
    def isServerAlive(self, timeout:int = -1)->bool:
        """ test if license server is alive """
        return gsIsServerAlive(timeout)

    def isValidSN(self, serial:str, timeout:int = -1)->bool:
        """ test if the serial number is a valid one """
        return gsIsSNValid(str2pchar(serial), timeout)

    def applySN(self, serial:str, timeout:int = -1)->bool:
        """ apply serial """
        rc = ctypes.c_int(0)
        ok = gsApplySN(str2pchar(serial), ctypes.byref(rc), None, timeout)
        
        print(f"applySN: rc: ({rc}) ok: {ok}")
        logging.debug(f"applySN: rc: ({rc}) ok: {ok}")

        return ok
    
    # ----- Offline Activation ------
    @core_must_inited
    def createRequest(self):
        """
        Create a request object
        """
        return Request(gsCreateRequest())

    def applyLicenseCode(self, code:str, serial:str)->bool:
        """ apply a license code from vendor """
        return gsApplyLicenseCodeEx(str2pchar(code), str2pchar(serial), None)

    @property 
    def unlockRequestCode(self)->str:
        """ request code to unlock all entities (the whole app) """
        req = self.createRequest()
        req.addAction(ActionId.ACT_UNLOCK)
        return req.code

    @property 
    def cleanRequestCode(self)->str:
        """ request code to clean up local license storage """
        req = self.createRequest()
        req.addAction(ActionId.ACT_CLEAN)
        return req.code

    @property 
    def fixRequestCode(self)->str:
        """ request code to fix license error """
        req = self.createRequest()
        req.addAction(ActionId.ACT_FIX)
        return req.code

    # license management

    def lockAllEntities(self):
        """ lock down all entities so the app cannot run until unlocked later """
        for e in self.entities:
            e.lock()

    def isAllEntitiesLocked(self)->bool:
        """ Are all entities already locked down? """
        return all((e.locked for e in self.entities))

    def isAllEntitiesUnlocked(self)->bool:
        """ Are all entities already unlocked (full purchased)? """
        return all((e.unlocked for e in self.entities))




