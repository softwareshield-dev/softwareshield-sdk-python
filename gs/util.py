""" Utility Helpers """

from ctypes import c_char_p
from .intf import gsCloseHandle

def mustbe(vtype, vname, v):
    """ make sure correct variable type """
    if not isinstance(v, vtype):
        raise TypeError(f"({vname}) must be of type ({vtype})!")

class one_call:
    """ plain function @staticmethod decorator to cache result of the first call 

        WARN: it should not be used for class member function, otherwise
        the cached result will be shared by all class instances!
    """
    def __init__(self, f):
        self._cached = False
        self._f = f
    
    def __call__(self, *args):
        if not self._cached:
            self._v = self._f(*args)
            self._cached = True
        return self._v

class once:
    """ class instance function decorator to cache result of the first call 

        WARN: it should not be used for plain function or @staticmethod/@classmethod, uses 'one_call' for best performance 
    """
    def __init__(self, f):
        self._cache = {}
        self._f = f
    
    def __call__(self, *args):
        # the first element of args should be object instance
        inst = args[0]
        try:
            return self._cache[inst]
        except KeyError:
            v= self._cache[inst] = self._f(*args)
            return v
            





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