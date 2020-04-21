from . import intf as _intf
from .util import SdkError, str2pchar
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
    """
    EVENT_ENTITY_TRY_ACCESS = 201

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
    if  eventId >= EventType.EVENT_TYPE_APP and eventId < EventType.EVENT_TYPE_ENTITY:
        return EventType.EVENT_TYPE_APP
    elif eventId < EventType.EVENT_TYPE_LICENSE:
        return EventType.EVENT_TYPE_ENTITY
    elif eventId < Event.EVENT_ID_MAX:
        return EventType.EVENT_TYPE_LICENSE

    return EventType.EVENT_TYPE_UNKNOWN


_hMonitor = None # internal monitor handle

@_intf.gs5_monitor_callback
def _gs_cb(eventId, hEvent, userData):
    print(f"event: {eventId} hEvent: {hEvent} userData: {userData}")

    eventType = getEventType(eventId)
    if eventType == EventType.EVENT_TYPE_UNKNOWN:
        logging.debug(f"Unknown eventId: {eventId}")
    elif eventType == EventType.EVENT_TYPE_APP:
        ...
    elif eventType == EventType.EVENT_TYPE_ENTITY:
        ...
    elif eventType == EventType.EVENT_TYPE_LICENSE:
        ...

        


def initMonitor():
    global _hMonitor
    if _hMonitor is None:
        _hMonitor = _intf.gsCreateMonitorEx(_gs_cb, None, str2pchar("sdk"))
        if _hMonitor is None:
            raise SdkError("global monitor creation failure")


class Monitor:
    pass 

class AppMonitor(Monitor):
    pass

class EntityMonitor(Monitor):
    pass

class LicenseMonitor(Monitor):
    pass
