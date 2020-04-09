""" License and License Model """

from .intf import *
from .util import *
from enum import IntEnum

class LicenseStatus(IntEnum):
    INVALID = -1 # The current status value is invalid /unknown
    LOCKED = 0   # the license is disabled permanently by lock() or already expired, the license model's logic is bypassed.
    UNLOCKED = 1 # the license is already unlocked, the license model's logic is bypassed.
    ACTIVE = 2   # the license model's logic is being used to decide if the protected entity is accessible

class License:
    def __init__(self, entity):
        self._entity = entity

        self._handle = gsOpenLicense(entity.handle)
        
        if not self._handle:
            raise RuntimeError("entity (%s) has no license attached" % (entity.name))

    def __del__(self):
        gsCloseHandle(self._handle)
    
    @property
    def handle(self):
        return self._handle

    @property
    def name(self):
        return pchar2str(gsGetLicenseName(self._handle))
    @property
    def id(self):
        return pchar2str(gsGetLicenseId(self._handle))
    @property
    def description(self):
        return pchar2str(gsGetLicenseDescription(self._handle))
    @property
    def entity(self):
        ''' the entity to protect '''
        return self._entity
    
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

    
    
