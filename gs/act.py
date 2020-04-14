"""
actions

To change license status, apply actions
"""

from enum import IntEnum

from .util import SdkError, HObject
from .intf import gsCloseHandle

class ActionId(IntEnum):
    """ unique action id """
    # Generic actions
    ACT_UNLOCK = 1
    ACT_LOCK = 2
    ACT_ENABLE_COPYPROTECTION = 6
    ACT_DISABLE_COPYPROTECTION = 7
    ACT_RESET_ALLEXPIRATION = 10
    ACT_CLEAN = 11
    ACT_DUMMY = 12
    ACT_PUSH = 13
    ACT_PULL = 14

    ACT_NAG_ON = 15
    ACT_NAG_OFF = 16
    ACT_ONE_SHOT = 17
    ACT_SHELFTIME= 18
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
    @property
    def id(self)->ActionId:
        """ unique action id """
        return self._id
    
    @staticmethod
    def create(actId: ActionId, handle):
        """ create action instance from its action-id """
        if _act_map[actId]:
            return _act_map[actId](handle)
        raise SdkError(f"action id ({actId}) not supported")




@act_id(ActionId.ACT_UNLOCK)
class Act_Unlock(Action):
    pass    