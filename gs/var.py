
from .intf import *
from .util import *

import ctypes
import logging
from datetime import datetime

from enum import IntEnum, IntFlag

class _VarAttr(IntFlag):
    READ = 1    # readable
    WRITE = 2   # writable
    PERSISTENT = 4  # persistent variable

class _VarType(IntEnum):
    UINT = 3    # unsigned int32
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
        print("typename: (%s)" % typstr)

        self._type = _VarType(gsGetVariableType(handle))
        self._attr = _VarAttr(gsGetVariableAttr(handle))
    
    def __del__(self):
        gsCloseHandle(self._handle)
    
    def __repr__(self):
        return "(%s) => %s" % (self.name, self.value)

    @property
    def name(self)->str:
        return pchar2str(gsGetVariableName(self._handle))
    @property
    def value(self)->any:
        if self._attr & _VarAttr.READ == 0:
            raise RuntimeError("variable (%s) not readable" % self.name)
        if not self.valid:
            raise RuntimeError("variable (%s) does not hold a valid value" % self.name)

        if self._type == _VarType.BOOL:
            v = ctypes.c_int()
            if gsGetVariableValueAsInt(self._handle, ctypes.byref(v)):
                return v.value != 0
        # int
        if self._type == _VarType.INT:
            v = ctypes.c_int()
            if gsGetVariableValueAsInt(self._handle, ctypes.byref(v)):
                return v.value
        
        if self._type == _VarType.INT64 or self._type == _VarType.UINT:
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
        if self._type == _VarType.TIME:
            v = ctypes.c_int64()
            if gsGetVariableValueAsInt64(self._handle, ctypes.byref(v)):
                return datetime.utcfromtimestamp(v.value)

        raise RuntimeError("Unsupported variable type, name (%s)" % self.name)

    @value.setter
    def value(self, v: any):
        if self._attr & _VarAttr.WRITE == 0:
            raise RuntimeError("variable (%s) not writable" % self.name)

        def raiseError():
            raise RuntimeError("variable (%s) set failure" % self.name)

        if self._type == _VarType.BOOL:
            mustbe(bool, 'v', v)
            if not gsSetVariableValueFromInt(self._handle, 1 if v else 0):
                raiseError()
        # int
        elif self._type == _VarType.INT:
            mustbe(int, 'v', v)
            if not gsSetVariableValueFromInt(self._handle, ctypes.c_int(v)):
                raiseError()
        
        elif self._type == _VarType.INT64 or self._type == _VarType.UINT:
            mustbe(int, 'v', v)
            if not gsSetVariableValueFromInt64(self._handle, ctypes.c_int64(v)):
                raiseError()
        
        elif self._type == _VarType.FLOAT:
            mustbe(float, 'v', v)
            if not gsSetVariableValueFromFloat(self._handle, ctypes.c_float(v)):
                raiseError()
        
        elif self._type == _VarType.DOUBLE:
            mustbe(float, 'v', v)
            if not gsSetVariableValueFromDouble(self._handle, ctypes.c_double(v)):
                raiseError()
        
        # string
        elif self._type == _VarType.STRING:
            mustbe(str, 'v', v)
            if not gsSetVariableValueFromString(self._handle, str2pchar(v)):
                raiseError()

        # time
        elif self._type == _VarType.TIME:
            mustbe(datetime, 'v', v)
            # 3.x:
            # timestamp = int(v.timestamp()+0.5)
            timestamp = int((v - datetime(1970, 1, 1)).total_seconds())
            if not gsSetVariableValueFromInt64(self._handle, ctypes.c_int64(timestamp)):
                raiseError()

        else:
            raise RuntimeError("Unsupported variable type, name (%s)" % self.name)

    @property
    def valid(self)->bool:
        """
        If the variable holds a valid value?

        some variable might not hold a valid value even the value itself looks valid. for example, if the variable holds a first-access timestamp of
        an app, its value won't be valid until the app is launched for the first time.
        """
        return gsIsVariableValid(self._handle)