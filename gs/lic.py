""" License and License Model """

from .intf import *
from .util import *


class License:
    def __init__(self, entity):
        self._entity = entity

        self._handle = gsOpenLicense(entity.handle)
        
        if not self._handle:
            raise RuntimeError("entity (%s) has no license attached" % (entity.name))
    
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
    def isValid(self):
        return gsIsLicenseValid(self._handle)
    @property
    def entity(self):
        ''' the entity to protect '''
        return self._entity

    def lock(self):
        ''' lock the license '''
        gsLockLicense(self._handle)