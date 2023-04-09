import cbase

from pylib0_xmzt import loglib

import clex_gen as gen

class TermStopException(Exception): pass

gen.TermStopException = TermStopException
exec('from cbase import *', gen.__dict__, gen.__dict__)

#======================================================================================================================
# Logc
#======================================================================================================================

class Logc:
    def ch__1(self, p, off, ch):
        return self.logr(f'[ch] <{p.src}+{off} {p.linePosS(p.src+off)}> {p.srcCh!r}')
    
    def errPos__1(self, p, pos, msg):
        return self.logr(f'[ERROR] <{pos} {p.linePosS(pos)}> {msg}')
    
    def errText__1(self, p, posA, posE, msg):
        return self.logr(f'[ERROR] <{posA} {p.linePosS(posA)}> {repr(p.srcA[posA:posE])} {msg}')
    
    def state__1(self, p, state):
        return self.logr(f'[state] {state.__name__}')
    
    def tokAdd__1(self, p):
        return self.logr(f'[tok] <{p.tokSrc} {p.linePosS(p.tokSrc)}> [{p.tokWs}] {p.tokTyp}')

    def tokAddAcc__1(self, p):
        return self.logr(f'[tok] <{p.tokSrc} {p.linePosS(p.tokSrc)}> [{p.tokWs}] {p.tokTyp}'
                         f' {p.accTyp} {p.accS!r}')
    
#======================================================================================================================
# Parser
#======================================================================================================================

class Parser:
    def __init__(self):
        # not in grammar directly
        self.accV = []
        self.accS = None
        self.lineSrcIV = [0]

        # in grammar and used by caller
        self.accTyp = None
        self.tokSrc = None
        self.tokTyp = None
        self.tokWs = None

        # only in grammar, not used by caller, e.g. temporary values
        self.bsSrc = None
        self.bsuI = None
        self.tmpU = None

    def go(self, srcA, src, state):
        self.srcA=srcA
        self.src=src
        try:
            while True:
                g_logc.state(self, state)
                state = state(self)
        except TermStopException:
            pass

    def acc(self, x):
        self.accV.append(x)

    def errPos(self, posA, msg):
        g_logc.errPos(self, posA, msg)

    def errText(self, posA, posE, msg):
        g_logc.errText(self, posA, posE, msg)

    def lineInc(self, off):
        self.lineSrcIV.append(self.src + off)

    def linePopGt(self):
        while self.lineSrcIV[-1] > self.src:
            self.lineSrcIV.pop()
            
    def linePosS(self, src):
        i = len(self.lineSrcIV)
        while True:
            i -= 1
            if (lineSrcI := self.lineSrcIV[i]) <= src:
                return f'{i}.{src - lineSrcI}'
            
    def tokAdd(self):
        g_logc.tokAdd(self)
        self.accV = []

    def tokAddAcc(self):
        self.accS = ''.join(self.accV)
        self.accV = []
        if cbase.TokTyp.Iden == self.tokTyp:
            self.tokTyp = cbase.TokTypByKeyword.get(self.accS, self.tokTyp)
        g_logc.tokAddAcc(self)
