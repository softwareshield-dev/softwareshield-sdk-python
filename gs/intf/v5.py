""" Interface to SDK v5 """

import ctypes

from ctypes import cdll, windll, WINFUNCTYPE
from ctypes.wintypes import LPCSTR, HANDLE, HMODULE, LPVOID, INT

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

gsCleanUp = WINFUNCTYPE(INT)((4, _hCore))
gsCloseHandle = WINFUNCTYPE(None)((5, _hCore))

gsGetLastErrorMessage = WINFUNCTYPE(LPCSTR)((7, _hCore))
gsGetLastErrorCode = WINFUNCTYPE(INT)((8, _hCore))



