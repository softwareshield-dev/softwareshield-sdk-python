""" Utility Helpers """

from ctypes import c_char_p

def mustbe(vt, vname, v):
    if not isinstance(v, vt):
        raise TypeError("(%s) must be of type (%s)!" % (vname, vt))

def str2pchar(v):
    return c_char_p(bytes(v, 'utf-8'))