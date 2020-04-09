""" 
Entity
"""

from .intf import *
from .util import *
from .lic import *
from enum import IntFlag


class EntityAttribute(IntFlag):
    ''' Entity Attribute '''
    ACCESSIBLE = 1 # Entity is currently accessible
    UNLOCKED = 2   # Entity's license is fully activated, no expire /trial limits at all.
    ACCESSING = 4  # Entity is active (being accessed via entity.beginAccess())
    LOCKED = 8     # Entity is locked (via entity.lock())
    AUTOSTART = 16 # Entity is auto-start (entity.beginAccess() is called automatically on app start)

class Entity:
    def __init__(self, handle):
        if handle is None:
            raise ValueError("Invalid entity handle")

        self._handle = handle

        # bundled license
        self._lic = License(self)

    def __del__(self):
        gsCloseHandle(self._handle)
    
    @property
    def handle(self):
        return self._handle

    @property
    def name(self):
        return pchar2str(gsGetEntityName(self._handle))
        
    @property
    def id(self):
        return pchar2str(gsGetEntityId(self._handle))
    
    @property
    def description(self):
        return pchar2str(gsGetEntityDescription(self._handle))

    def beginAccess(self):
        """
         Try start accessing an entity.
         returns true if the entity is accessed successfully.
         returns false if license attached to this entity is invalid.

        This api can be called recursively, and each call must be paired with an endAccess().
        """
        return gsBeginAccessEntity(self._handle)
        
    def endAccess(self):
        """
        Try end accessing an entity
        """
        return gsEndAccessEntity(self._handle)

    # License
    @property
    def license(self):
        return self._lic

    def lock(self):
        """ lock the entity's license """
        self.license.lock()

    # attribute and helpers
    @property
    def attribute(self):
        return EntityAttribute(gsGetEntityAttributes(self._handle))

    @property
    def accessible(self):
        """ entity can be accessed """
        return self.attribute & EntityAttribute.ACCESSIBLE != 0

    @property
    def locked(self):
        """ entity is already locked
          entity can be locked after its license is expired or manually locked (via Entity.lock())
        """
        return self.attribute & EntityAttribute.LOCKED != 0
    
    @property
    def unlocked(self):
        """ entity is already unlocked """
        return self.attribute & EntityAttribute.UNLOCKED != 0

    @property
    def accessing(self):
        """ entity is being accessed """
        return self.attribute & EntityAttribute.ACCESSING != 0
    
    @property
    def autoStart(self):
        """ entity is auto-started """
        return self.attribute & EntityAttribute.AUTOSTART != 0

        
