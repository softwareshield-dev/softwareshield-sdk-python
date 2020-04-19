""" Interface to SDK v5 """

import ctypes

from ctypes import cdll, windll, WINFUNCTYPE
from ctypes.wintypes import LPCSTR, HANDLE, HMODULE, LPVOID, INT, DWORD, UINT, BOOL, BYTE
from ctypes import c_bool, POINTER

import os


def _tryLoadCore():
    ''' Load gsCore lib to process '''
    # load core lib from current working directory
    core_path = os.path.join(os.getcwd(), "gscore")
    print(f"try loading core lib({core_path})...")

    hCore = None

    try:
        if os.name == 'nt':
            hCore = windll.LoadLibrary(core_path)
        else:
            hCore = cdll.LoadLibrary(core_path)
    except:
        # load core lib from PATH
        if os.name == 'nt':
            print("\ntry loading core from PATH...")

            try:
                handle = windll.kernel32.LoadLibraryW("gscore")
                print(f"Handle={hex(handle)}")
                if handle:
                    hCore = ctypes.WinDLL("gscore", handle=handle)
            except Exception as ex:
                print(ex)

    return hCore

_hCore = _tryLoadCore()

if _hCore is None:
    raise RuntimeError("Core lib cannot be loaded!")




"""""""""""""""""""""""
 Prototypes
"""""""""""""""""""""""
gsGetVersion = WINFUNCTYPE(LPCSTR)((2, _hCore))

gsInit = WINFUNCTYPE(INT, LPCSTR, LPCSTR, LPCSTR, LPVOID)((3, _hCore))
gsInitEx = WINFUNCTYPE(INT, LPCSTR, LPVOID, INT, LPCSTR, LPVOID)((103, _hCore))

gsCleanUp = WINFUNCTYPE(INT)((4, _hCore))
gsCloseHandle = WINFUNCTYPE(None, HANDLE)((5, _hCore))

gsFlush = WINFUNCTYPE(None)((6, _hCore))

gsGetLastErrorMessage = WINFUNCTYPE(LPCSTR)((7, _hCore))
gsGetLastErrorCode = WINFUNCTYPE(INT)((8, _hCore))

gsGetBuildId = WINFUNCTYPE(INT)((9, _hCore))
gsGetProductName = WINFUNCTYPE(LPCSTR)((84, _hCore))
gsGetProductId = WINFUNCTYPE(LPCSTR)((85, _hCore))

# Entity
gsGetEntityCount = WINFUNCTYPE(INT)((10, _hCore))

gsOpenEntityByIndex = WINFUNCTYPE(HANDLE, INT)((11, _hCore))
gsOpenEntityById = WINFUNCTYPE(HANDLE, LPCSTR)((12, _hCore))

gsGetEntityAttributes = WINFUNCTYPE(DWORD, HANDLE)((13, _hCore))
gsGetEntityId = WINFUNCTYPE(LPCSTR, HANDLE)((14, _hCore))
gsGetEntityName = WINFUNCTYPE(LPCSTR, HANDLE)((15, _hCore))
gsGetEntityDescription = WINFUNCTYPE(LPCSTR, HANDLE)((16, _hCore))

gsBeginAccessEntity = WINFUNCTYPE(c_bool, HANDLE)((20, _hCore))
gsEndAccessEntity = WINFUNCTYPE(c_bool, HANDLE)((21, _hCore))

# License
gsOpenLicense = WINFUNCTYPE(HANDLE, HANDLE)((137, _hCore))
gsGetLicenseId = WINFUNCTYPE(LPCSTR, HANDLE)((28, _hCore))
gsGetLicenseName = WINFUNCTYPE(LPCSTR, HANDLE)((22, _hCore))
gsGetLicenseDescription = WINFUNCTYPE(LPCSTR, HANDLE)((23, _hCore))
gsGetLicenseStatus = WINFUNCTYPE(DWORD, HANDLE)((24, _hCore))
gsIsLicenseValid = WINFUNCTYPE(c_bool, HANDLE)((34, _hCore))

gsLockLicense = WINFUNCTYPE(None, HANDLE)((138, _hCore))

gsGetLicenseParamCount = WINFUNCTYPE(INT, HANDLE)((29, _hCore))
gsGetLicenseParamByIndex = WINFUNCTYPE(HANDLE, HANDLE, INT)((30, _hCore))
# Variable
gsGetVariable = WINFUNCTYPE(HANDLE, LPCSTR)((52, _hCore))
gsGetVariableName = WINFUNCTYPE(LPCSTR, HANDLE)((53, _hCore))
gsGetVariableType = WINFUNCTYPE(BYTE, HANDLE)((54, _hCore))
gsVariableTypeToString = WINFUNCTYPE(LPCSTR, BYTE)((55, _hCore))
gsGetVariableAttr = WINFUNCTYPE(INT, HANDLE)((56, _hCore))
gsIsVariableValid = WINFUNCTYPE(c_bool, HANDLE)((67, _hCore))

gsGetVariableValueAsString = WINFUNCTYPE(LPCSTR, HANDLE)((57, _hCore))
gsSetVariableValueFromString = WINFUNCTYPE(c_bool, HANDLE, LPCSTR)((58, _hCore))

gsGetVariableValueAsInt = WINFUNCTYPE(c_bool, HANDLE, POINTER(ctypes.c_int))((59, _hCore))
gsSetVariableValueFromInt = WINFUNCTYPE(c_bool, HANDLE, ctypes.c_int)((60, _hCore))

gsGetVariableValueAsInt64 = WINFUNCTYPE(c_bool, HANDLE, POINTER(ctypes.c_int64))((61, _hCore))
gsSetVariableValueFromInt64 = WINFUNCTYPE(c_bool, HANDLE, ctypes.c_int64)((62, _hCore))

gsGetVariableValueAsFloat = WINFUNCTYPE(c_bool, HANDLE, POINTER(ctypes.c_float))((63, _hCore))
gsSetVariableValueFromFloat = WINFUNCTYPE(c_bool, HANDLE, ctypes.c_float)((64, _hCore))

gsGetVariableValueAsDouble = WINFUNCTYPE(c_bool, HANDLE, POINTER(ctypes.c_double))((78, _hCore))
gsSetVariableValueFromDouble = WINFUNCTYPE(c_bool, HANDLE, ctypes.c_double)((79, _hCore))

gsGetVariableValueAsTime = WINFUNCTYPE(c_bool, HANDLE, POINTER(ctypes.c_uint64))((68, _hCore))
gsSetVariableValueFromTime = WINFUNCTYPE(c_bool, HANDLE, ctypes.c_uint64)((69, _hCore))

# Request
gsCreateRequest = WINFUNCTYPE(HANDLE)((36, _hCore))
gsAddRequestAction = WINFUNCTYPE(HANDLE, HANDLE, BYTE, HANDLE)((37, _hCore))
gsGetRequestCode = WINFUNCTYPE(LPCSTR, HANDLE)((45, _hCore))

# action
gsGetActionInfoCount = WINFUNCTYPE(INT, HANDLE)((32, _hCore))
gsGetActionInfoByIndex = WINFUNCTYPE(LPCSTR, HANDLE, INT, POINTER(ctypes.c_byte))((33, _hCore))

gsGetActionName = WINFUNCTYPE(LPCSTR, HANDLE)((38, _hCore))
gsGetActionDescription = WINFUNCTYPE(LPCSTR, HANDLE)((40, _hCore))
gsGetActionString = WINFUNCTYPE(LPCSTR, HANDLE)((41, _hCore))

gsGetActionParamCount = WINFUNCTYPE(INT, HANDLE)((42, _hCore))
gsGetActionParamByIndex = WINFUNCTYPE(HANDLE, HANDLE, INT)((44, _hCore))

# online activation
gsIsServerAlive = WINFUNCTYPE(c_bool, INT)((131, _hCore))
gsApplySN = WINFUNCTYPE(c_bool, LPCSTR, POINTER(ctypes.c_int), POINTER(ctypes.c_char_p), INT)((133, _hCore))
gsIsSNValid = WINFUNCTYPE(c_bool, LPCSTR, INT)((139, _hCore))

# offline activation
gsApplyLicenseCodeEx = WINFUNCTYPE(c_bool, LPCSTR, LPCSTR, LPCSTR)((158, _hCore))