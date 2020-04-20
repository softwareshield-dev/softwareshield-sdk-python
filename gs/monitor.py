from .intf import gsCreateMonitorEx, gs5_monitor_callback
from .util import SdkError, str2pchar

@gs5_monitor_callback
def _gs_cb(eventId, hEvent, userData):
    print(f"event: {eventId}")

def initMonitor():
    h = gsCreateMonitorEx(_gs_cb, None, str2pchar("sdk"))
    if h is None:
        raise SdkError("global monitor creation failure")

