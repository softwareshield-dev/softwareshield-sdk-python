"""
actions

To change license status, apply actions
"""

from enum import IntEnum

from .util import *
from .intf import *
from .var import Variable

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
    def __init__(self, handle):
        super().__init__(handle)
        self._params = None # later param binding
    
    @staticmethod
    def create(actId: ActionId, handle):
        """ create action instance from its action-id """
        if _act_map[actId]:
            return _act_map[actId](handle)
        raise SdkError(f"action id ({actId}) not supported")
    
    @property
    def id(self)->ActionId:
        """ unique action id """
        return self._id
    
    @property
    def name(self):
        """ action name """
        return pchar2str(gsGetActionName(self._handle))

    @property
    def params(self):
        """ action parameters """
        if self._params is None:
            self._params = { x.name: x for x in [ Variable(gsGetActionParamByIndex(self._handle, i)) for i in range(gsGetActionParamCount(self._handle)) ] }
        return self._params


#----------- Generic Actions ----------------------
@act_id(ActionId.ACT_UNLOCK)
class Act_Unlock(Action): pass    

@act_id(ActionId.ACT_LOCK)
class Act_Lock(Action): pass    

@act_id(ActionId.ACT_CLEAN)
class Act_Clean(Action): pass    

@act_id(ActionId.ACT_DUMMY)
class Act_Dummy(Action): pass    

@act_id(ActionId.ACT_FIX)
class Act_Fix(Action): pass    

#----------- Trial License Actions ----------------------
@act_id(ActionId.ACT_RESET_ALLEXPIRATION)
class Act_ResetAllExpiration(Action): pass    

@act_id(ActionId.ACT_ADD_ACCESSTIME)
class Act_AddAccessTime(Action): pass    

@act_id(ActionId.ACT_SET_ACCESSTIME)
class Act_SetAccessTime(Action): pass    

@act_id(ActionId.ACT_SET_STARTDATE)
class Act_SetStartDate(Action): pass    

@act_id(ActionId.ACT_SET_ENDDATE)
class Act_SetEndDate(Action): pass    

@act_id(ActionId.ACT_SET_SESSIONTIME)
class Act_SetSessionTime(Action): pass    

@act_id(ActionId.ACT_SET_EXPIRE_PERIOD)
class Act_SetPeriod(Action): pass    

@act_id(ActionId.ACT_ADD_EXPIRE_PERIOD)
class Act_AddPeriod(Action): pass    

@act_id(ActionId.ACT_SET_EXPIRE_DURATION)
class Act_SetDuration(Action): pass    

@act_id(ActionId.ACT_ADD_EXPIRE_DURATION)
class Act_AddDuration(Action): pass    