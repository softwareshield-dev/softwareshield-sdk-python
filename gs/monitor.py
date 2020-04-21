from . import intf as _intf
from .util import SdkError, str2pchar

_hMonitor = None # internal monitor handle

@_intf.gs5_monitor_callback
def _gs_cb(eventId, hEvent, userData):
    print(f"event: {eventId} hEvent: {hEvent} userData: {userData}")

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
