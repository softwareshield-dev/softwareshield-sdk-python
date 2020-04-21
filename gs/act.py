"""
actions

To change license status, apply actions
"""

from enum import IntEnum

from .util import pchar2str, once, HObject, SdkError
from . import intf as _intf
from .var import Variable
from datetime import datetime

class ActionId(IntEnum):
    """ unique action id """
    # Generic actions
    ACT_UNLOCK = 1
    ACT_LOCK = 2
    ACT_RESET_ALLEXPIRATION = 10
    ACT_CLEAN = 11
    ACT_DUMMY = 12

    ACT_FIX = 19

    # LM-specific actions

    # LM.expire.accessTime
    ACT_ADD_ACCESSTIME = 100
    ACT_SET_ACCESSTIME = 101

    # LM.expire.hardDate
    ACT_SET_STARTDATE = 102
    ACT_SET_ENDDATE = 103

    # LM.expire.session
    ACT_SET_SESSIONTIME = 104

    # LM.expire.period
    ACT_SET_EXPIRE_PERIOD = 105
    ACT_ADD_EXPIRE_PERIOD = 106

    # LM.expire.duration
    ACT_SET_EXPIRE_DURATION = 107
    ACT_ADD_EXPIRE_DURATION = 108


_act_map = {}

class act_id:
    """ action id decorator """
    def __init__(self, id):
        self._id = id

    def __call__(self, cls):
        cls.id = self._id
        _act_map[self._id] = cls
        return cls


class Action(HObject):
    _id = None

    def __init__(self, handle):
        super().__init__(handle)

    def __repr__(self):
        return '\n'.join([f"{type(self).__name__}({self.id}): {self.name}", *[f"{self.params[x]}" for x in self.params]])

    
    @staticmethod
    def create(actId: ActionId, handle):
        """ create action instance from its action-id """
        if _act_map[actId]:
            return _act_map[actId](handle)
        raise SdkError(f"action id ({actId}) not supported")
    
    @property
    def id(self)->ActionId:
        """ unique action id """
        if self._id is None:
            raise SdkError("action id not specified, please use decorator 'act_id()'")
        return self._id
    
    @property
    @once
    def name(self):
        """ action name """
        return pchar2str(_intf.gsGetActionName(self._handle))

    @property
    @once
    def params(self):
        """ action parameters """
        return { x.name: x for x in [ Variable(_intf.gsGetActionParamByIndex(self._handle, i)) for i in range(_intf.gsGetActionParamCount(self._handle)) ] }


#----------- Generic Actions ----------------------
@act_id(ActionId.ACT_UNLOCK)
class Act_Unlock(Action): pass    

@act_id(ActionId.ACT_LOCK)
class Act_Lock(Action): pass    

@act_id(ActionId.ACT_CLEAN)
class Act_Clean(Action):
    @property
    def hasExpireDate(self)->bool:
        """ does action has expire date? """
        return self.params['endDate'].valid

    @property
    def expireDate(self)->datetime:
        """ expire date of this action """
        return self.params['endDate'].value

    @expireDate.setter
    def expireDate(self, dt: datetime):
        """ setup expire date """
        self.params['endDate'].value = dt

@act_id(ActionId.ACT_DUMMY)
class Act_Dummy(Action): pass    

@act_id(ActionId.ACT_FIX)
class Act_Fix(Action): pass    

#----------- Trial License Actions ----------------------
@act_id(ActionId.ACT_RESET_ALLEXPIRATION)
class Act_ResetAllExpiration(Action): pass    

@act_id(ActionId.ACT_ADD_ACCESSTIME)
class Act_AddAccessTime(Action):
    @property
    def addedTimes(self)->int:
        """how many times to add """
        return self.params['addedAccessTime'].value

    @addedTimes.setter
    def addedTimes(self, v:int):
        """ setup how many times to add """
        self.params['addedAccessTime'].value = v 


@act_id(ActionId.ACT_SET_ACCESSTIME)
class Act_SetAccessTime(Action):
    @property
    def times(self)->int:
        """how many times to set """
        return self.params['newAccessTime'].value

    @times.setter
    def times(self, v:int):
        """ setup how many times to access """
        self.params['newAccessTime'].value = v 


@act_id(ActionId.ACT_SET_STARTDATE)
class Act_SetStartDate(Action): 
    @property
    def hasStartDate(self)->bool:
        """ does action has start date specified? """
        return self.params['startDate'].valid
    @property
    def startDate(self)->datetime:
        """ When the license becomes valid? 
            Only available for scenerio 'ValidBetween' and 'ValidSince'
        """
        return self.params['startDate'].value

    @startDate.setter
    def startDate(self, v:datetime):
        """ setup the start point license will be valid"""
        self.params['startDate'].value = v 


@act_id(ActionId.ACT_SET_ENDDATE)
class Act_SetEndDate(Action):
    @property
    def hasEndDate(self)->bool:
        """ does action has ending date specified? """
        return self.params['endDate'].valid

    @property
    def endDate(self)->datetime:
        """ when the license will be expired? (alias of property 'expireDate')
            Only available for scenerio 'ValidBetween' and 'ExpireAfter'
        """
        return self.params['endDate'].value

    @endDate.setter
    def endDate(self, v:datetime):
        """ setup the time when the license will be expired"""
        self.params['endDate'].value = v 

@act_id(ActionId.ACT_SET_SESSIONTIME)
class Act_SetSessionTime(Action):
    @property
    def sessionTime(self)->int:
        """ return new session time in seconds """
        return self.params['newSessionTime'].value
    
    @sessionTime.setter
    def sessionTime(self, v:int):
        """ sets new session time in seconds """
        self.params['newSessionTime'].value = v

@act_id(ActionId.ACT_SET_EXPIRE_PERIOD)
class Act_SetPeriod(Action):
    @property
    def period(self)->int:
        """ return new period in seconds """
        return self.params['newPeriodInSeconds'].value

    @period.setter
    def period(self, v:int):
        """ sets new period in seconds """
        self.params['newPeriodInSeconds'].value = v

@act_id(ActionId.ACT_ADD_EXPIRE_PERIOD)
class Act_AddPeriod(Action):    
    @property
    def addedPeriod(self)->int:
        """ return added period in seconds """
        return self.params['addedPeriodInSeconds'].value
        
    @addedPeriod.setter
    def addedPeriod(self, v:int):
        """ set added period in seconds """
        self.params['addedPeriodInSeconds'].value = v

@act_id(ActionId.ACT_SET_EXPIRE_DURATION)
class Act_SetDuration(Action):  
    @property
    def duration(self)->int:
        """ return new duration in seconds """
        return self.params['duration'].value
        
    @duration.setter
    def duration(self, v:int):
        """ sets new duration in seconds """
        self.params['duration'].value = v

@act_id(ActionId.ACT_ADD_EXPIRE_DURATION)
class Act_AddDuration(Action):
    @property
    def addedDuration(self)->int:
        """ return added duration in seconds """
        return self.params['addedDuration'].value
        
    @addedDuration.setter
    def addedDuration(self, v:int):
        """ set added duration in seconds """
        self.params['addedDuration'].value = v