"""SoftwareShield core api"""

import ctypes

from ctypes import cdll, windll, WINFUNCTYPE
from ctypes.wintypes import LPCSTR, HANDLE, HMODULE, LPVOID

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
    raise RuntimeError("Core lib cannot load!")




"""""""""""""""""""""""
 Prototypes
"""""""""""""""""""""""
gsGetVersion = WINFUNCTYPE(LPCSTR)((2, _hCore))


def getVersion():
    return str(gsGetVersion(),'utf-8')
