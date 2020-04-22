from . import intf as _intf
from .util import SdkError, str2pchar
from .entity import Entity

from enum import IntFlag 

import logging
class Event(IntFlag):
    """ System Event IDs """

    # ******** App Events ********

    # Application just gets started, please initialize
    EVENT_APP_BEGIN = 1
    # Application is going to terminate, last signal before game exits.
    EVENT_APP_END = 2
    # Alarm: Application detects the clock is rolled back
    EVENT_APP_CLOCK_ROLLBACK = 3
    # Fatal Error: Application integrity is corrupted.
    EVENT_APP_INTEGRITY_CORRUPT = 4
    # Application starts to run, last signal before game code is executing
    EVENT_APP_RUN = 5

    # ILdrCore [INTERNAL]
    EVENT_PASS_BEGIN_RING1 = 20
    EVENT_PASS_BEGIN_RING2 = 22

    EVENT_PASS_END_RING1 = 21
    EVENT_PASS_END_RING2 = 24

    EVENT_PASS_CHANGE = 23


    # ******** License Events ********
    EVENT_IDBASE_LICENSE = 100
    # Original license is uploaded to license store for the first time.
    EVENT_LICENSE_NEWINSTALL = 101
    # The application's license store is connected /initialized successfully (gsCore::gsInit() == 0)
    EVENT_LICENSE_READY = 102

    # The application's license store cannot be connected /initialized! (gsCore::gsInit() != 0)
    EVENT_LICENSE_FAIL = 103

    # License is loading...
    EVENT_LICENSE_LOADING = 105

    # ******** Entity Events ********
    EVENT_IDBASE_ENTITY = 200

    """
    *
    * The entity is to be accessed.
    *
    * The listeners might be able to modify the license store here.
    * The internal licenses status are untouched. (inactive if not accessed before)
    * 
    * (alias: EVENT_ENTITY_TRY_ACCESS)
    """
    EVENT_ENTITY_ACCESS_STARTING = 201

    """
    *
    * The entity is being accessed.
    *
    * The listeners can enable any protected resources here. (inject decrypting keys, etc.)
    * The internal licenses status have changed to active mode.
    *
    """
    EVENT_ENTITY_ACCESS_STARTED = 202

    """
    *
    * The entity is leaving now.
    *
    * The listeners can revoke any protected resources here. (remove injected decrypting keys, etc.)
    * Licenses are still in active mode.
    *"""
    EVENT_ENTITY_ACCESS_ENDING = 203

    """
    *
    * The entity is deactivated now.
    *
    * The listeners can revoke any protected resources here. (remove injected decrypting keys, etc.)
    * Licenses are kept in inactive mode.
    *
    """
    EVENT_ENTITY_ACCESS_ENDED = 204

    # Alarm: Entity access invalid (due to expiration, etc)
    EVENT_ENTITY_ACCESS_INVALID = 205
    # Internal ping event indicating entity is still alive.
    EVENT_ENTITY_ACCESS_HEARTBEAT = 206

    """
    *
    * The status of attached licenses have been modified by applying license action.
    *
    * It is called after the change has been made.
    *
    *"""
    EVENT_ENTITY_ACTION_APPLIED = 208


    EVENT_ID_MIN = 0
    EVENT_ID_MAX = 1000

class EventType(IntFlag):
    EVENT_TYPE_UNKNOWN = -1

    EVENT_TYPE_APP = 0
    EVENT_TYPE_LICENSE = 100
    EVENT_TYPE_ENTITY = 200

def getEventType(eventId: int)->EventType:
    """ Get event type from event id """
    if  eventId >= EventType.EVENT_TYPE_APP and eventId < EventType.EVENT_TYPE_LICENSE:
        return EventType.EVENT_TYPE_APP
    elif eventId < EventType.EVENT_TYPE_ENTITY:
        return EventType.EVENT_TYPE_LICENSE
    elif eventId < Event.EVENT_ID_MAX:
        return EventType.EVENT_TYPE_ENTITY

    return EventType.EVENT_TYPE_UNKNOWN


# Event Listeners
_appListeners = {}
_entityListeners = {}
_licListeners = {}

# entity event decorators
class entity_listener(object):
    _event: Event = None

    def __init__(self, f):
        # save native function to be decorated so that when calling no recursion occurs
        self._f = f if not isinstance(f, entity_listener) else f._f
        try:
            _entityListeners[self._event].append(self)
        except KeyError:
            _entityListeners[self._event] = [self]

    def __call__(self, entity: Entity, event):
        self._f(entity, event)

class entity_access_starting(entity_listener):
    _event = Event.EVENT_ENTITY_ACCESS_STARTING

class entity_access_started(entity_listener):
    _event = Event.EVENT_ENTITY_ACCESS_STARTED

class entity_access_ending(entity_listener):
    _event = Event.EVENT_ENTITY_ACCESS_ENDING
    
class entity_access_ended(entity_listener):
    _event = Event.EVENT_ENTITY_ACCESS_ENDED
    
class entity_access_invalid(entity_listener):
    _event = Event.EVENT_ENTITY_ACCESS_INVALID

# alias for more intuitive meaning for trial license model
trial_expired = entity_access_invalid

class entity_access_heartbeat(entity_listener):
    _event = Event.EVENT_ENTITY_ACCESS_HEARTBEAT

class entity_action_applied(entity_listener):
    _event = Event.EVENT_ENTITY_ACTION_APPLIED


# license event decorators
class license_listener(object):
    _event: Event = None

    def __init__(self, f):
        # save native function to be decorated so that when calling no recursion occurs
        self._f = f if not isinstance(f, license_listener) else f._f
        try:
            _licListeners[self._event].append(self)
        except KeyError:
            _licListeners[self._event] = [self]

    def __call__(self, event):
        self._f(event)


class license_loading(license_listener):
    _event = Event.EVENT_LICENSE_LOADING

class license_loaded(license_listener):
    _event = Event.EVENT_LICENSE_READY

class license_new_install(license_listener):
    _event = Event.EVENT_LICENSE_NEWINSTALL

class license_fail(license_listener):
    _event = Event.EVENT_LICENSE_FAIL

# application event decorators
class app_listener(object):
    _event: Event = None

    def __init__(self, f):
        # save native function to be decorated so that when calling no recursion occurs
        self._f = f if not isinstance(f, app_listener) else f._f
        try:
            _appListeners[self._event].append(self)
        except KeyError:
            _appListeners[self._event] = [self]

    def __call__(self, event):
        self._f(event)

class app_begin(app_listener):
    _event = Event.EVENT_APP_BEGIN

class app_end(app_listener):
    _event = Event.EVENT_APP_END

class app_run(app_listener):
    _event = Event.EVENT_APP_RUN

class app_clock_rollbacked(app_listener):
    _event = Event.EVENT_APP_CLOCK_ROLLBACK

class app_integrity_corrupted(app_listener):
    _event = Event.EVENT_APP_INTEGRITY_CORRUPT

#=================================================================    
_hMonitor = None # internal monitor handle


def _resolveEntity(hEvent, event)->Entity:
    """ resolve entity from hEvent (handle to entity event) """
    hEntity = _intf.gsGetEventSource(hEvent)
    if hEntity is None:
        raise SdkError(f"entity event ({event}) cannot resolve event source")

    # first check if the entity already exists in core
    from .core import Core
    for e in Core().entities:
        if e.handle == hEntity:
            return e
    # create an entity instance as last resort
    return Entity(hEntity)

@_intf.gs5_monitor_callback
def _gs_cb(eventId, hEvent, userData):
    event = Event(eventId)
    print(f"event: {event} hEvent: {hEvent} userData: {userData}")

    eventType = getEventType(eventId)

    if eventType == EventType.EVENT_TYPE_UNKNOWN:
        logging.debug(f"Unknown eventId: {eventId}")
    elif eventType == EventType.EVENT_TYPE_APP:
        try:
            listeners = _appListeners[eventId]
            if len(listeners) > 0:
                for x in listeners:
                    x(event)
        except KeyError:
            pass # no listeners

    elif eventType == EventType.EVENT_TYPE_ENTITY:
        try:
            listeners = _entityListeners[eventId]
            if len(listeners) > 0:
                entity = _resolveEntity(hEvent, event)
                for x in listeners:
                    x(entity, event)
        except KeyError:
            pass # no listeners

    elif eventType == EventType.EVENT_TYPE_LICENSE:
        try:
            listeners = _licListeners[eventId]
            if len(listeners) > 0:
                for x in listeners:
                    x(event)
        except KeyError:
            pass # no listeners

        


def initMonitor():
    global _hMonitor
    if _hMonitor is None:
        _hMonitor = _intf.gsCreateMonitorEx(_gs_cb, None, str2pchar("sdk"))
        if _hMonitor is None:
            raise SdkError("global monitor creation failure")

