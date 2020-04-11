""" Utility Helpers """

from ctypes import c_char_p

def mustbe(vtype, vname, v):
    if not isinstance(v, vtype):
        raise TypeError(f"({vname}) must be of type ({vtype})!")

def str2pchar(v):
    """ Convert str to char* """
    p = c_char_p(bytes(v, 'utf-8'))
    return p
    #return c_char_p(bytes(v, 'utf-8'))

def pchar2str(pstr):
    """ Convert char* to str """
    return str(pstr, 'utf-8')