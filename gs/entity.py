""" 
Entity
"""

from .intf import *
from .util import *

class Entity:

    def __init__(self, handle):
        self._handle = handle
    
    @property
    def name(self):
        return pchar2str(gsGetEntityName(self._handle))
        
    @property
    def id(self):
        return pchar2str(gsGetEntityId(self._handle))
    
    @property
    def description(self):
        return pchar2str(gsGetEntityDescription(self._handle))
        
