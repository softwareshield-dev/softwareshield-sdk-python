"""SoftwareShield core api"""

import ctypes

from ctypes import cdll, windll, WINFUNCTYPE
from ctypes.wintypes import LPCSTR

import os

_hCore = None

# load core lib from current working directory
core_path = os.path.join(os.getcwd(), "gscore")
print("try loading core lib(%s)..." % core_path)

try:
    if os.name == 'nt':
        _hCore = windll.LoadLibrary(core_path)
    else:
        _hCore = cdll.LoadLibrary(core_path)
except Exception as ex:
    print(ex)


# load core lib from PATH
if _hCore == None:
    if os.name == 'nt':
        print("\ntry loading core from PATH...")

        try:
            handle = windll.kernel32.LoadLibraryW("gscore")
            print("Handle=%s" % hex(handle))
            if handle:
                _hCore = ctypes.WinDLL("gscore", handle=handle)

        except Exception as ex:
            print(ex)

if _hCore == None:
    raise RuntimeError("Core lib cannot load!")




"""""""""""""""""""""""
 Prototypes
"""""""""""""""""""""""

gsGetVersion = WINFUNCTYPE(LPCSTR)(_hCore[2])




def getVersion():
    return str(gsGetVersion(),'utf-8')