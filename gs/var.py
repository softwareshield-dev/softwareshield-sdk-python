
from .intf import *
from .util import *

import ctypes
import logging

from enum import IntEnum, IntFlag

class _VarAttr(IntFlag):
    READ = 1    # readable
    WRITE = 2   # writable
    PERSISTENT = 4  # persistent variable

class _VarType(IntEnum):
    INT = 7     # 32bit-integer
    INT64 = 8   # 64bit integer
    FLOAT = 9   # float
    DOUBLE = 10 # double
    BOOL = 11   # bool
    STRING = 20 # ansi-string
    TIME = 30   # datetime


class Variable:
    """
    User defined variable (UDV)
    """
    def __init__(self, handle):
        if handle is None:
            raise ValueError("variable handle cannot be empty!")

        self._handle = handle
        typ = gsGetVariableType(handle)
        typstr = pchar2str(gsVariableTypeToString(typ))
        logging.debug("typename: (%s)" % typstr)

        self._type = _VarType(gsGetVariableType(handle))
        self._attr = _VarAttr(gsGetVariableAttr(handle))
    
    def __del__(self):
        gsCloseHandle(self._handle)
    
    @staticmethod
    def get(name):
        h = gsGetVariable(str2pchar(name))
        if h is None:
            raise ValueError("variable (%s) not found" % name)

        return Variable(h)

    @property
    def name(self):
        return pchar2str(gsGetVariableName(self._handle))
    @property
    def value(self):
        # int
        if self._type == _VarType.INT:
            v = ctypes.c_int()
            if gsGetVariableValueAsInt(self._handle, ctypes.byref(v)):
                return v.value
        
        if self._type == _VarType.INT64:
            v = ctypes.c_int64()
            if gsGetVariableValueAsInt64(self._handle, ctypes.byref(v)):
                return v.value
        
        if self._type == _VarType.FLOAT:
            v = ctypes.c_float()
            if gsGetVariableValueAsFloat(self._handle, ctypes.byref(v)):
                return v.value
        
        if self._type == _VarType.DOUBLE:
            v = ctypes.c_double()
            if gsGetVariableValueAsDouble(self._handle, ctypes.byref(v)):
                return v.value
        
        # string
        if self._type == _VarType.STRING:
            return pchar2str(gsGetVariableValueAsString(self._handle))

        # time
        if self._type == _VarType.TIME:pass


        raise RuntimeError("Unsupported variable type, name (%s)" % self.name)