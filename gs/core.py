"""SoftwareShield core api"""


from .intf import *
from ctypes import *
from .util import *


def getVersion():
    return str(gsGetVersion(),'utf-8')


def init(productId, pathToLic, password):
    mustbe(str, "productId", productId)
    mustbe(str, "pathToLic", pathToLic)
    mustbe(str, "password", password)

    return gsInit(str2pchar(productId), str2pchar(pathToLic), str2pchar(password),None) == 0
