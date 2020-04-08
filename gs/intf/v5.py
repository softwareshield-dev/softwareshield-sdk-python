""" Interface to SDK v5 """

import ctypes

from ctypes import cdll, windll, WINFUNCTYPE
from ctypes.wintypes import LPCSTR, HANDLE, HMODULE, LPVOID, INT, DWORD, UINT, BOOL
from ctypes import c_bool

import os


def _tryLoadCore():
    ''' Load gsCore lib to process '''
    # load core lib from current working directory
    core_path = os.path.join(os.getcwd(), "gscore")
    print("try loading core lib(%s)..." % core_path)

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
                print("Handle=%s" % hex(handle))
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




