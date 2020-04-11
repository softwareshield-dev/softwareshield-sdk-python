""" License and License Model """

from .intf import *
from .util import *
from .var import *

from enum import IntEnum, Enum
from datetime import timedelta, datetime

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



class License:
    def __init__(self, entity):
        self._entity = entity

        self._handle = gsOpenLicense(entity.handle)
        if not self._handle:
            raise RuntimeError(f"entity ({entity.name}) has no license attached")

        self._name = pchar2str(gsGetLicenseName(self._handle))
        self._id = LicenseId(pchar2str(gsGetLicenseId(self._handle)))
        self._description = pchar2str(gsGetLicenseDescription(self._handle))

        # params
        self._params = None # late-binding

        self._inspector = None

    def __del__(self):
        gsCloseHandle(self._handle)
    
    @property
    def handle(self):
        return self._handle

    @property
    def name(self):
        return self._name
    @property
    def id(self):
        return self._id
    @property
    def description(self):
        return self._description
    @property
    def entity(self):
        ''' the entity to protect '''
        return self._entity

    @property
    def params(self):
        if self._params is None:
            self._params = { x.name: x for x in [Variable(gsGetLicenseParamByIndex(self._handle, i)) for i in range(gsGetLicenseParamCount(self._handle))] }
        return self._params
    
    @property
    def valid(self):
        return gsIsLicenseValid(self._handle)

    @property
    def status(self):
        return LicenseStatus(gsGetLicenseStatus(self._handle))
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
        gsLockLicense(self._handle)

    @property
    def inspector(self):
        # license inspector for more details 
        if self._inspector is None:
            self._inspector = _Inspectors[self.id](self)
        return self._inspector
    
# License Model Inspectors

@inspect(LicenseId.TRIAL_PERIOD)
class LM_Period:
    """
    Trial By Period license inspector
    """
    def __init__(self, lic: License):
        self._lic = lic
    
    def __repr__(self):
        if self.used:
            return f'''
                used: {self.used} \n
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
        # entity has been accessed before
        return self._lic.params['timeFirstAccess'].valid

    @property 
    def expirePeriodInSeconds(self)->int:
        # trial period settings in seconds
        return self._lic.params['periodInSeconds'].value

    @property 
    def secondsLeft(self)->int:
        # how many seconds left before license is expired
        x = self.expirePeriodInSeconds - self.secondsPassed
        return x if x >=0 else 0

    @property 
    def secondsPassed(self)->int:
        # how many seconds has elapsed since entity was first accessed
        # return 0 if entity is never accessed before
        return 0 if not self.used else int((datetime.utcnow() - self.firstAccessDate).total_seconds())

    @property 
    def firstAccessDate(self)->datetime:
        # the first time entity is accessed
        if self.used:
            return self._lic.params['timeFirstAccess'].value
        raise ValueError("entity is never accessed before")

    @property 
    def expireDate(self)->datetime:
        # when the license will be expired?
        return self.firstAccessDate + timedelta(seconds=self.expirePeriodInSeconds)