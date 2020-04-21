"""
Request code
"""

from . import intf as _intf
from .util import HObject, SdkError, pchar2str
from .entity import Entity
from .act import ActionId, Action

class Request(HObject):
    """ request code generator """

    def addAction(self, actId: ActionId, target: Entity = None):
        """
        Create an action object with an optional target entity

        If target is not specified, then all entities are targetted
        """
        if target and isinstance(target, Entity) and not target.license.acceptAction(actId):
            raise SdkError(f"Action (id: {actId}) cannot be accepted by target entity ({target.name})")

        hLic = None if target is None else target.license.handle
        hAct = _intf.gsAddRequestAction(self._handle, actId, hLic)
        if hAct is None:
            entityName = 'all entities' if target is None else f"entity {target.name}"
            raise SdkError(f"Action (id: {actId}) cannot be added to request targetting {entityName}")

        return Action.create(actId, hAct)
    
    @property
    def code(self)->str:
        """ request code """
        return pchar2str(_intf.gsGetRequestCode(self._handle))