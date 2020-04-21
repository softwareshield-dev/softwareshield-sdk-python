
from . import intf as _intf
from .util import SdkError, HObject, once, pchar2str, str2pchar, mustbe

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


class Variable(HObject):
    """
    User defined variable (UDV)
    """
    def __init__(self, handle):
        super().__init__(handle)

        typ = _intf.gsGetVariableType(handle)
        typstr = pchar2str(_intf.gsVariableTypeToString(typ))
        logging.debug(f"typename: ({typstr})")

        self._type = _VarType(_intf.gsGetVariableType(handle))
        self._attr = _VarAttr(_intf.gsGetVariableAttr(handle))
    
    def __repr__(self):
        vstr = "N/A" if not self.valid else self.value
        return f"{self.name} => {vstr}"

    @property
    @once
    def name(self)->str:
        return pchar2str(_intf.gsGetVariableName(self._handle))
        
    @property
    def value(self)->any:
        if self._attr & _VarAttr.READ == 0:
            raise SdkError(f"variable ({self.name}) not readable")
        if not self.valid:
            raise SdkError(f"variable ({self.name}) does not hold a valid value")

        if self._type == _VarType.BOOL:
            v = ctypes.c_int()
            if _intf.gsGetVariableValueAsInt(self._handle, ctypes.byref(v)):
                return v.value != 0
        # int
        if self._type == _VarType.INT:
            v = ctypes.c_int()
            if _intf.gsGetVariableValueAsInt(self._handle, ctypes.byref(v)):
                return v.value
        
        if self._type == _VarType.INT64 or self._type == _VarType.UINT:
            v = ctypes.c_int64()
            if _intf.gsGetVariableValueAsInt64(self._handle, ctypes.byref(v)):
                return v.value
        
        if self._type == _VarType.FLOAT:
            v = ctypes.c_float()
            if _intf.gsGetVariableValueAsFloat(self._handle, ctypes.byref(v)):
                return v.value
        
        if self._type == _VarType.DOUBLE:
            v = ctypes.c_double()
            if _intf.gsGetVariableValueAsDouble(self._handle, ctypes.byref(v)):
                return v.value
        
        # string
        if self._type == _VarType.STRING:
            return pchar2str(_intf.gsGetVariableValueAsString(self._handle))

        # time
        if self._type == _VarType.TIME:
            v = ctypes.c_int64()
            if _intf.gsGetVariableValueAsInt64(self._handle, ctypes.byref(v)):
                return datetime.utcfromtimestamp(v.value)

        raise SdkError(f"Unsupported variable type, name ({self.name})")

    @value.setter
    def value(self, v: any):
        if self._attr & _VarAttr.WRITE == 0:
            raise SdkError(f"variable ({self.name}) not writable")

        def raiseError():
            raise SdkError(f"variable ({self.name}) set failure")

        if self._type == _VarType.BOOL:
            mustbe(bool, 'v', v)
            if not _intf.gsSetVariableValueFromInt(self._handle, 1 if v else 0):
                raiseError()
        # int
        elif self._type == _VarType.INT:
            mustbe(int, 'v', v)
            if not _intf.gsSetVariableValueFromInt(self._handle, ctypes.c_int(v)):
                raiseError()
        
        elif self._type == _VarType.INT64 or self._type == _VarType.UINT:
            mustbe(int, 'v', v)
            if not _intf.gsSetVariableValueFromInt64(self._handle, ctypes.c_int64(v)):
                raiseError()
        
        elif self._type == _VarType.FLOAT:
            mustbe(float, 'v', v)
            if not _intf.gsSetVariableValueFromFloat(self._handle, ctypes.c_float(v)):
                raiseError()
        
        elif self._type == _VarType.DOUBLE:
            mustbe(float, 'v', v)
            if not _intf.gsSetVariableValueFromDouble(self._handle, ctypes.c_double(v)):
                raiseError()
        
        # string
        elif self._type == _VarType.STRING:
            mustbe(str, 'v', v)
            if not _intf.gsSetVariableValueFromString(self._handle, str2pchar(v)):
                raiseError()

        # time
        elif self._type == _VarType.TIME:
            mustbe(datetime, 'v', v)
            # 3.x:
            # timestamp = int(v.timestamp()+0.5)
            timestamp = int((v - datetime(1970, 1, 1)).total_seconds())
            if not _intf.gsSetVariableValueFromInt64(self._handle, ctypes.c_int64(timestamp)):
                raiseError()

        else:
            raise SdkError(f"Unsupported variable type, name ({self.name})")

    @property
    def valid(self)->bool:
        """
        If the variable holds a valid value?

        some variable might not hold a valid value even the value itself looks valid. for example, if the variable holds a first-access timestamp of
        an app, its value won't be valid until the app is launched for the first time.
        """
        return _intf.gsIsVariableValid(self._handle)