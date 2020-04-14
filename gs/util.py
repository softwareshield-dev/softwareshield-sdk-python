""" Utility Helpers """

from ctypes import c_char_p
from .intf import gsCloseHandle

def mustbe(vtype, vname, v):
    if not isinstance(v, vtype):
        raise TypeError(f"({vname}) must be of type ({vtype})!")

def str2pchar(v):
    """ Convert str to char* """
    p = c_char_p(bytes(v, 'utf-8'))
    return p
    #return c_char_p(bytes(v, 'utf-8'))

def pchar2str(pstr):
    """ Convert char* to str """
    return str(pstr, 'utf-8')

# the root of all SDK errors
class SdkError(RuntimeError):pass

class HObject:
    """ Wrapper Object with handle from sdk core """
    def __init__(self, handle):
        if handle is None:
            raise SdkError("SDK Object's handle cannot be empty!")
        self._handle = handle
    def __del__(self):
        gsCloseHandle(self._handle)

    @property
    def handle(self):
        """ internal handle """
        return self._handle