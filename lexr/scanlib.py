from __main__ import g_logc

import chtab
import objlib
import util

import re

#======================================================================================================================
# exceptions
#======================================================================================================================

class InputStopException(Exception): pass

class DqNtermException(Exception): pass #(srcI) 
class PlNtermException(Exception): pass #(srcI)
class SqNtermException(Exception): pass #(srcI)

#======================================================================================================================
# Scanr
#======================================================================================================================

class Scanr:
    def __init__(self, mach, accRoot, src, srcA=0):
        self.mach = mach
        self.acc1 = self.accRoot = accRoot
        self.src = src
        self.srcA = self.srcE = srcA
        #self.srcCh
        self.stack = []
        self.eolIgnore = False
        self.posE = 0
        self.posEolV = [0]
        
    def acc(self, obj):
        g_logc.scanObj(obj)
        self.acc1(obj)

    def chIn(self):
        self.srcA = self.srcE
        if self.srcA >= len(self.src):
            raise InputStopException()
        self.srcE += 1
        self.srcCh = self.src[self.srcA]
        g_logc.scanChIn(self)
        return self.srcCh

    def diag(self):
        return objlib.DiagScanr(self, self.srcA, self.srcE)
    
    def go(self):
        state = f_start
        try:
            while True:
                g_logc.scanState(self, state)
                state = state(self)
        except InputStopException:
            pass
        if self.stack:
            raise PlNtermException(self.lst.srcA)
        self.acc(objlib.EofObj(self.mach, self.diag()))
        
    def objFromPy(self, x):
        try:
            y = int(x)
        except:
            pass
        else:
            return objlib.IntLitObj(self.mach, self.diag(), y)
        try:
            y = float(x)
        except:
            pass
        else:
            return objlib.FloatLitObj(self.mach, self.diag(), y)
        return objlib.BareObj(self.mach, self.diag(), x)
    
    def srcPos(self, posX):
        # lazy conversion of pos to (zero-based) line and column when asked for by pretty-printer.
        # scanner does not need to keep track of eol.
        # keeps a vector of pos after each eol.
        # this is efficient if pos greater than in any previous call.
        # todo: make efficient for pos=0 when entire file has been read
        while posX >= self.posE:
            if -1 == (x := self.src.index('\n', self.posE)):
                # entire file has been processed. subsequent calls skip straight to EolV check.
                self.srcPos = self.posFromEolV
            else:
                x += 1
                self.posEolV.append(x)
                self.posE = x
        return self.posFromEolV(posX)
            
    def posFromEolV(self, posX):
        posL = len(self.posEolV)-1
        while 0 > (posC := posX - self.posEolV[posL]):
            posL -= 1
        return f'{posL}.{posC}/{posX}'

#======================================================================================================================
# f_* and Lut_* make up a parse table. why would someone leave goto out of a language?
#======================================================================================================================

DqRe = re.compile(r'(?:(?:\\.)|[^\"])*?\"', re.S)
SqRe = re.compile(r"(?:(?:\\.)|[^\'])*?\'", re.S)
EolRe = re.compile(r'\n|$', re.S) # causes m.end() to be after eol unlike ('$', re.M)
BareRe = re.compile(r'''[^ \t\r\n\#()\[\]{}\"\']*''', re.S)

def f_start(self):
    return Lut_ws.get(self.chIn(), f_bare)

def f_ws_eol(self):
    self.acc(objlib.EolObj(self.mach, self.diag()))
    return f_start

def f_ws_Bs(self):
    return f_bs

def f_ws_Has(self):
    self.srcE = EolRe.search(self.src, self.srcE).end()
    return f_start

def f_Pl(self):
    g_logc.scanStack(self, 1)
    lst = objlib.LstObj(self.mach, self.diag(), [])
    self.stack.append((self.acc1, lst))
    self.acc1 = lst.scanAcc
    return f_start

def f_Pr(self):
    g_logc.scanStack(self, -1)
    self.acc1,lst = self.stack.pop()
    lst.diag.srcE = self.srcE
    self.acc(lst)
    return f_start
        
def f_Sbl(self):
    self.srcE = chtab.chsetParse(chDset := {}, self.src, self.srcE)
    self.acc(objlib.ChsetObj(self.mach, self.diag(), chDset))
    return f_start

def f_Dq(self):
    if not (m := DqRe.match(self.src, self.srcE)):
        raise DqNtermException(self.srcA)
    self.srcE = m.end()
    self.acc(objlib.StrLitObj(self.mach, self.diag(), eval(self.src[self.srcA:self.srcE])))
    return f_start

def f_Sq(self):
    if not (m := SqRe.match(self.src, self.srcE)):
        raise SqNtermException(self.srcA)
    self.srcE = m.end()
    self.acc(objlib.StrLitObj(self.mach, self.diag(), eval(self.src[self.srcA:self.srcE])))
    return f_start

def f_bare(self):
    self.srcE = BareRe.match(self.src, self.srcE).end()
    self.acc(self.objFromPy(self.src[self.srcA:self.srcE]))
    return f_start

def f_bs(self):
    self.bsBackA,self.bsBackE = self.srcA,self.srcE
    return Lut_bs.get(self.chIn(), f_bs_other)

def f_bs_eol(self):
    return f_start

def f_bs_other(self):
    self.srcA,self.srcE = self.bsBackA,self.bsBackE
    return f_bare(self)

Lut_ws = { ' ':f_start, '\t':f_start, '\r':f_start, '\n':f_ws_eol, '#':f_ws_Has, '\\':f_ws_Bs,
           '(':f_Pl, ')':f_Pr, '[':f_Sbl, '"':f_Dq, "'":f_Sq }

Lut_bs = { ' ':f_bs, '\t':f_bs, '\r':f_bs, '\n':f_bs_eol }
