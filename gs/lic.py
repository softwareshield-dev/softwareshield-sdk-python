""" License and License Model """

from . import intf as _intf
from .util import SdkError, pchar2str, str2pchar, HObject, once
from .var import Variable
from .act import ActionId

from enum import IntEnum, Enum
from datetime import timedelta, datetime
import ctypes


class LicenseId(Enum):
    # trial license models
    TRIAL_ACCESS = 'gs.lm.expire.accessTime.1'
    TRIAL_SESSION = 'gs.lm.expire.sessionTime.1'
    TRIAL_DURATION = 'gs.lm.expire.duration.1'
    TRIAL_PERIOD = 'gs.lm.expire.period.1'
    TRIAL_HARDDATE = 'gs.lm.expire.hardDate.1'

    #non-trial models
    ALWAYS_RUN = 'gs.lm.alwaysRun.1'
    ALWAYS_LOCK = 'gs.lm.alwaysLock.1'


class LicenseStatus(IntEnum):
    INVALID = -1 # The current status value is invalid /unknown
    LOCKED = 0   # the license is disabled permanently by lock() or already expired, the license model's logic is bypassed.
    UNLOCKED = 1 # the license is already unlocked, the license model's logic is bypassed.
    ACTIVE = 2   # the license model's logic is being used to decide if the protected entity is accessible

# LicenseId -> Inspector map
_Inspectors = {}
class inspect:
    '''
    decorator to associate inspector with license
    '''
    def __init__(self, licId: LicenseId):
        self._id = licId

    def __call__(self, cls):
        _Inspectors[self._id] = cls
        return cls



class License(HObject):
    def __init__(self, entity):
        self._entity = entity

        h = _intf.gsOpenLicense(entity.handle)
        if not h:
            raise SdkError(f"entity ({entity.name}) has no license attached")

        super().__init__(h)


        # actions acceptable by this license model
        n = _intf.gsGetActionInfoCount(h)
        self._act_ids = []
        for i in range(n):
            act_id = ctypes.c_byte(0)
            p = _intf.gsGetActionInfoByIndex(h, i, ctypes.byref(act_id))
            if p:
                self._act_ids.append(act_id.value)

    @property
    @once
    def name(self):
        return pchar2str(_intf.gsGetLicenseName(self._handle))

    @property
    @once
    def id(self):

        return LicenseId(pchar2str(_intf.gsGetLicenseId(self._handle)))
    @property
    @once
    def description(self):
        return pchar2str(_intf.gsGetLicenseDescription(self._handle))
        
    @property
    def entity(self):
        ''' the entity to protect '''
        return self._entity

    @property
    @once
    def params(self):
        return { x.name: x for x in [Variable(_intf.gsGetLicenseParamByIndex(self._handle, i)) for i in range(_intf.gsGetLicenseParamCount(self._handle))] }
    
    @property
    def valid(self):
        return _intf.gsIsLicenseValid(self._handle)

    @property
    def status(self):
        return LicenseStatus(_intf.gsGetLicenseStatus(self._handle))
    # status helper
    @property
    def locked(self):
        return self.status == LicenseStatus.LOCKED
    @property
    def expired(self):
        return self.status == LicenseStatus.LOCKED
    @property
    def unlocked(self):
        return self.status == LicenseStatus.UNLOCKED

    def lock(self):
        ''' lock the license '''
        _intf.gsLockLicense(self._handle)

    @property
    @once
    def inspector(self):
        # license inspector for more details 
        return _Inspectors[self.id](self)

    def acceptAction(self, actId: ActionId)->bool:
        """ can action be applied to this license model? """
        return actId in self._act_ids

    @property
    def unlockRequestCode(self)->str:
        """ the request code to unlock this license only """
        from .core import Core
        req = Core().createRequest()
        req.addAction(ActionId.ACT_UNLOCK, self.entity)
        return req.code

    
# License Model Inspectors
class Inspector:
    def __init__(self, lic: License):
        self._lic = lic


@inspect(LicenseId.ALWAYS_LOCK)
class LM_Lock(Inspector): pass

@inspect(LicenseId.ALWAYS_RUN)
class LM_Run(Inspector): pass


class TrialInspector(Inspector):
    @property
    def exitAppOnExpired(self)->bool:
        """ app will be terminated once license becomes expired by sdk core """
        return self._lic.params['exitAppOnExpire'].value


@inspect(LicenseId.TRIAL_ACCESS)
class LM_Access(TrialInspector):
    @property
    def maxTimes(self)->int:
        """ total times allowed to access the entity """
        return self._lic.params['maxAccessTimes'].value

    @property
    def timesUsed(self)->int:
        """ how many times consumed accessing the entity """
        return self._lic.params['usedTimes'].value

    @property
    def timesLeft(self)->int:
        """ how many times left to access the entity """
        return self.maxTimes - self.timesUsed

@inspect(LicenseId.TRIAL_DURATION)
class LM_Duration(TrialInspector):
    def __init__(self, lic: License):
        self._lic = lic

    @property
    def duration(self)->int:
        """ how many seconds allowed to access the entity """
        return self._lic.params['maxDurationInSeconds'].value

    @property
    def secondsPassed(self)->int:
        """ how many seconds accumulated since entity is accessed """
        return self._lic.params['usedDurationInSeconds'].value

    @property
    def secondsLeft(self)->int:
        """ how many seconds left to access the entity """
        return 0 if self.secondsPassed >= self.duration else self.duration - self.secondsLeft


@inspect(LicenseId.TRIAL_HARDDATE)
class LM_HardDate(TrialInspector):

    class Scenario(Enum):
        VaidBetween = 1 # valid between (tBegin, tEnd)
        ExpireAfter = 2 # valid until tEnd, tBegin undefined
        ValidSince  = 3 # valid since tBegin, tEnd undefined


    def __init__(self, lic: License):
        self._lic = lic
        
        # three valid scenarios (ref: http://doc.softwareshield.com/UG/license_action.html#expire_by_harddate)
        if lic.params['timeBeginEnabled'].value:
            if lic.params['timeEndEnabled'].value:
                self._scenario = LM_HardDate.Scenario.VaidBetween
            else:
                self._scenario = LM_HardDate.Scenario.ValidSince
        else:
            if lic.params['timeEndEnabled'].value:
                self._scenario = LM_HardDate.Scenario.ExpireAfter
            else:
                raise SdkError("Invalid license parameters")

    @property
    def timeBegin(self)->datetime:
        """ When the license becomes valid? 
            Only available for scenerio 'ValidBetween' and 'ValidSince'
        """

        if self._scenario == LM_HardDate.Scenario.ExpireAfter:
            raise SdkError("timeBegin not defined for scenario 'ExpireAfter'")

        return self._lic.params['timeBegin'].value

    @property
    def timeEnd(self)->datetime:
        """ when the license will be expired? (alias of property 'expireDate')
            Only available for scenerio 'ValidBetween' and 'ExpireAfter'
        """
        if self._scenario == LM_HardDate.Scenario.ValidSince:
            raise SdkError("timeEnd not defined for scenario 'ValidSince'")

        return self._lic.params['timeEnd'].value

    @property
    def secondsLeft(self)->int:
        """
         how many seconds left before license is expired (ValidBetween / ExpireAfter)
         or how many seconds left before license is valid (ValidSince)
        """
        t = datetime.utcnow()
        if self._scenario == LM_HardDate.Scenario.ValidSince:
            return 0 if t >= self.timeBegin else int((self.timeBegin - t).total_seconds())
        else:
            return 0 if t >= self.timeEnd else int((self.timeEnd - t).total_seconds())
    @property 
    def expireDate(self)->datetime:
        """ when the license will be expired? (alias of property 'timeEnd') """
        return self.timeEnd


@inspect(LicenseId.TRIAL_SESSION)
class LM_Session(TrialInspector):
    def __init__(self, lic: License):
        self._lic = lic
    @property
    def secondsPassed(self)->int:
        """Session time elapsed in seconds"""
        return self._lic.params['sessionTimeUsed'].value
    @property
    def secondsTotal(self)->int:
        """ maximum seconds allowed in a session """
        return self._lic.params['maxSessionTime'].value
    @property
    def secondsLeft(self)->int:
        """ how many seconds left before this session expires """
        return 0 if self.secondsPassed >= self.secondsTotal else self.secondsTotal - self.secondsPassed
    @property 
    def expireDate(self)->datetime:
        """ when the license will be expired for this session? """
        return datetime.now() + self.secondsLeft
    

@inspect(LicenseId.TRIAL_PERIOD)
class LM_Period(TrialInspector):
    """
    Trial By Period license inspector
    """
    def __init__(self, lic: License):
        self._lic = lic
    
    def __repr__(self):
        if self.used:
            return f'''
                used: {self.used} \n
                exitAppOnExpired: {self.exitAppOnExpired} \n
                expirePeriodInSeconds: {self.expirePeriodInSeconds} \n
                secondsLeft: {self.secondsLeft} \n
                secondsPassed: {self.secondsPassed} \n
                firstAccessDate: {self.firstAccessDate} \n
                expireDate: {self.expireDate} '''
        else:
            return f'''
                used: {self.used} \n
                expirePeriodInSeconds: {self.expirePeriodInSeconds} \n
                secondsLeft: {self.secondsLeft} \n
                secondsPassed: {self.secondsPassed} \n
                firstAccessDate: N/A \n
                expireDate: N/A '''


    @property
    def used(self)->bool:
        """ entity has been accessed before """
        return self._lic.params['timeFirstAccess'].valid

    @property 
    def expirePeriodInSeconds(self)->int:
        """ trial period settings in seconds """
        return self._lic.params['periodInSeconds'].value

    @property 
    def secondsLeft(self)->int:
        """ how many seconds left before license is expired """
        x = self.expirePeriodInSeconds - self.secondsPassed
        return x if x >=0 else 0

    @property 
    def secondsPassed(self)->int:
        """
         how many seconds has elapsed since entity was first accessed
         return 0 if entity is never accessed before
        """
        return 0 if not self.used else int((datetime.utcnow() - self.firstAccessDate).total_seconds())

    @property 
    def firstAccessDate(self)->datetime:
        """ the first time entity is accessed """
        if self.used:
            return self._lic.params['timeFirstAccess'].value
        raise SdkError("entity is never accessed before")

    @property 
    def expireDate(self)->datetime:
        """ when the license will be expired? """
        return self.firstAccessDate + timedelta(seconds=self.expirePeriodInSeconds)