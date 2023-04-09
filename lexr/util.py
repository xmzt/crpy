import chtab

from pylib0_xmzt import loglib

import collections
import re
import sys
import subprocess

class ArgNBadException(Exception): pass 

def a_and_b(a,b): return a & b

def des0(x):
    if None is not (f := getattr(x, 'des0', None)):
        return f()
    #elif isinstance(x, list):
    #    return f'({" ".join([des0(y) for y in x])})'
    else:
        return repr(x)

def desTyp(x):
    if None is not (f := getattr(x, 'desTyp', None)):
        return f()
    else:
        return f'<{x.__class__.__name__}>{des0(x)}'

def desTypSrc(x):
    if None is not (f := getattr(x, 'desTypSrc', None)):
        return f()
    else:
        return desTyp(x)

def desCall(argV, **kwds):
    acc = []
    for arg in argV:
        acc.append(des0(arg))
    for k,v in kwds.items():
        acc.append(f'{k}={des0(v)}')
    return f'({" ".join(acc)})'
    
def desMeth(self, f): return 

def dumpArgV(argV, logr, pre):
    with logr(pre):
        for i,arg in enumerate(argV):
            logr(f'[arg {i}] {arg!r}')
    return logr

def dumpDict(d, logr, pre):
    with logr(f'{pre}'):
        for k,v in d.items():
            logr(f'{k}: {v!r}')
        
def dumpObjDir(obj, logr, pre):
    with logr(f'{pre}0x{id(obj):x} {obj!r}'):
        for k in dir(obj):
            try:
                logr(f'{k}: {getattr(obj, k)}')
            except:
                logr(f'{k}: {sys.exc_info()[1]!r}')

MangleRe = re.compile(r'([A-Za-z0-9_]+)|(.)', re.S)
def mangle(iden):
    return '_'.join([ chtab.name1(x) if (x := m.group(2)) else m.group(1) for m in MangleRe.finditer(iden) ])

def raiseArgNGt(argV, n):
    if len(argV) > n:
        raise ArgNBadException(f'{len(argV)}>{n}')
        
def raiseArgNLt(argV, n):
    if len(argV) < n:
        raise ArgNBadException(f'{len(argV)}<{n}')

def raiseArgNNe(argV, n):
    if len(argV) != n:
        raise ArgNBadException(f'{len(argV)}/{n}')

def reduceOrRunP(a, b): return a | b.runP()

#========================================================================================================================# as main

if __name__ == '__main__':
    pys = 'actlib cbase chtab clex codepylib funlib logclib machlib nodelib objlib scanlib util'
    subprocess.run(['wc'] + [f'{x}.py' for x in pys.split()])
