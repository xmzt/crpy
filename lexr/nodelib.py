from __main__ import g_logc

import chtab
import objlib
import util

from pylib0_xmzt import loglib

import functools

# WS 'a': ToFroKey or TofroKeyNset
# WS 'a' op: op calls tran.toCondOrNew and then works on the tranTo of that.
# WS 'ab' on 'a' calls tran.to.tranByKey('b') or creates cond first
# tran.tranByKey on an op fails - require cond to be explicitly added

#======================================================================================================================
# constants 
#======================================================================================================================

OffNset = -1
OffMulti = -2

TranPrioMax = 1<<62

#======================================================================================================================
# exceptions
#======================================================================================================================

class StopOffNready(Exception): pass

class OffSearchSrcAssignNdeterminedException(Exception): pass #(searchr)
class OffSearchSrcAssignConflictException(Exception): pass #(searchr, node)

class TranChainToAlreadyException(Exception): #(tran,to)
    def __str__(self):
        return f'\ntran={util.desTyp(self.args[0])}\nto={util.desTyp(self.args[1])}\n'

class TranVerifyException(Exception): pass #(tran)
class TranVerifyToException(Exception): pass #(tran, to)

#class TranToNsetException(Exception): pass
#class TranKeyTranInvalidException(Exception): pass

#======================================================================================================================
# helpers
#======================================================================================================================

class OffSearchSrcAssignr:
    def __init__(self, node0, target):
        self.node0 = node0
        self.target = target
        self.off = OffNset
        
    def des0(self):
        return util.desCall([self.__class__.__name__, self.node0, self.target], off=self.off)

def reduceTranPrioIden(a, b): return a if a.prioIden() <= b.prioIden() else b
def reduceTranPrioDump(a, b): return a if a.prioDump() <= b.prioDump() else b

def dumpOff(tran, offExpect):
    return '' if offExpect == tran.off else f'[off={tran.off}]'

#======================================================================================================================
# NodeBase
#======================================================================================================================

class NodeBase(objlib.ObjBase):
    def __init__(self, mach, diag):
        super().__init__(mach, diag)
        self.froTranV = []
        self.mach.nodeUniqI += 1
        self.uniq = self.mach.nodeUniqI
        self.mark = None

    def asNode(self):
        return self

    def des0(self):
        return f'{self.uniq}/{self.iden()}'

    def dumpNodeTree(self, logr, pre, ind, froTran):
        if (self.mark != self.mach.mark
            and functools.reduce(reduceTranPrioDump, self.froTranV, froTranFavNone) is froTran):
            self.mark = self.mach.mark
            self.dumpNodeTreeFull(logr, pre, ind)
        else:
            logr(f'{pre}[to] {self.des0()}')

    def froTranAppend(self, tran):
        self.froTranV.append(tran)
        
    def froTranRemove(self, tran):
        self.froTranV.remove(tran)

    def iden(self):
        return self.iden1({})

    def iden1(self, loopD):
        a,b = self.idenAB(loopD)
        return a if 0 == b else f'{a}+{b}'
        
    def idenAB(self, loopD):
        if id(self) in loopD:
            return f'<loop {" ".join([str(node.uniq) for node in loopD.values()])}>',0
        loopD[id(self)] = self
        return functools.reduce(reduceTranPrioIden, self.froTranV, froTranFavNone).idenAB(loopD)

    def replace(self, repl):
        self.removeFwd()
        for tran in (froTranV := self.froTranV):
            tran.to = repl
            repl.froTranAppend(tran)
        self.froTranV = []
        return froTranV
    
    def unredunKey0(self):
        return (self.uniq,)

    def verify(self):
        if self.mark != self.mach.mark:
            self.mark = self.mach.mark
            self.mach.verifyN += 1
            self.verify1()
            
#======================================================================================================================
# NodeNset

class NodeNset(NodeBase):
    def froTranAppend(self, tran):
        super().froTranAppend(tran)
        
    def froTranRemove(self, tran):
        super().froTranRemove(tran)

    def idenAB(self, loopD): return '<Nset>',0

    def offSet(self, off): pass

    def verify(self): pass
    
#======================================================================================================================
# NodeCodeMix

class NodeCodeMix:
    def codePyFun(self, logr):
        with logr(f'def f{self.uniq}(self): #{self.iden()}'):
            self.codePyFunMeat(logr)
            logr(f'return f{self.tranTo.to.uniq} #{self.tranTo.to.iden()}')
            
    def codePyLut(self, logr): pass

#======================================================================================================================
# NodeTerm

class NodeTerm(NodeBase):
    def idenAB(self, loopD): return '<Term>',0

    def offSet(self, off): pass

    def verify(self): pass

#======================================================================================================================
# NodeTo: abstract

class NodeTo(NodeBase):
    def __init__(self, mach, diag):
        super().__init__(mach, diag)
        self.off = OffNset 
        self.offFwd = OffNset
        self.mach.nodeDset[id(self)] = self
        #self.tranTo set by subclass init
        
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        prev.chainTo(self)
        chainV[chainI].chain(chainV, chainI+1, self)
        
    #def chainKey(self, key)

    def chainTo(self, to):
        return self.tranTo.chainTo(to)

    def chainToSameTo(self, node):
        return self.tranTo.chainToSameTo(node)
    
    def chainToOk(self):
        return self.tranTo.chainToOk()
    
    def chainTranOffSet(self, off):
        self.tranTo.off = off
    
    def condNemptyP(self):
        return 0

    def desDumpNodeTree(self):
        return f'{self.des0()} [{self.off}] <{self.__class__.__name__}>'

    def dumpNodeTreeHead(self, logr, pre):
        with logr(f'{pre}{self.desDumpNodeTree()}'):
            if g_logc.dumpNodeTreeFro:
                logr(f'froTranV: {" ".join([tran.desFro() for tran in self.froTranV])}')
    
    def dumpNodeTreeFull(self, logr, pre, ind):
        self.dumpNodeTreeHead(logr, pre)
        with logr if ind else loglib.logNoop:
            self.tranTo.to.dumpNodeTree(logr, dumpOff(self.tranTo, 0), 0, self.tranTo)

    def removeFwd(self):
        self.tranTo.to.froTranRemove(self.tranTo)

    def offSearchSrcAssign(self, target):
        searchr = OffSearchSrcAssignr(self, target)
        with g_logc.offSearchSrcAssign0(searchr):
            self.mach.mark += 1
            self.offSearchSrcAssignFro(searchr)
            if OffNset == searchr.off:
                raise OffSearchSrcAssignNdeterminedException(searchr)
            g_logc.offSearchSrcAssignRes(searchr)
            return searchr.off
            
    def offSearchSrcAssign1(self, searchr):
        if self.mark != self.mach.mark:
            self.mark = self.mach.mark
            match = self.offSearchSrcAssignMatchP(searchr)
            g_logc.offSearchSrcAssign1(self, match)
            if match:
                if OffNset == self.off:
                    raise StopOffNready()
                elif OffNset == searchr.off:
                    searchr.off = self.off
                elif searchr.off != self.off:
                    raise OffSearchSrcAssignConflictException(searchr, self)
            else:
                self.offSearchSrcAssignFro(searchr)

    def offSearchSrcAssignFro(self, searchr):
        for tran in self.froTranV:
            tran.offSearchSrcAssignFro(searchr)

    def offSearchSrcAssignMatchP(self, searchr):
        return False
        
    def offProp(self):
        try:
            self.offFwd = self.off
            self.offPropModFwd()
        except StopOffNready:
            self.offFwd = OffNset
            self.mach.offPropDset[id(self)] = self
        else:
            self.offPropFwd()
                
    def offPropFwd(self):
        self.tranTo.offSet(self.offFwd)
        
    def offPropModFwd(self): pass

    def offMultiOk(self):
        return False

    def offMultiOk_1(self):
        return True
    
    def offSet(self, off):
        if OffNset == self.off:
            if OffMulti != off or self.offMultiOk():
                self.off = off
                g_logc.offSet(self)
                self.mach.offPropDset[id(self)] = self
            else:
                self.mach.offErrDset[id(self)] = self
        elif off != self.off:
            if not self.offMultiOk():
                self.mach.offErrDset[id(self)] = self
            elif OffMulti != self.off:
                self.off = OffMulti
                g_logc.offSet(self)
                self.mach.offPropDset[id(self)] = self

    def verify1(self):
        for tran in self.froTranV:
            if tran.to is not self:
                raise TranVerifyToException(tran, self)
        self.tranTo.verify()

#======================================================================================================================
# NodeToNset

class NodeToNset(NodeTo):
    def __init__(self, mach, diag):
        super().__init__(mach, diag)
        self.tranTo = TranToFroNset(mach, diag, mach.nodeNset, self, None, 0).reg()

#======================================================================================================================
# NodeToTerm

class NodeToTerm(NodeCodeMix, NodeTo):
    def __init__(self, mach, diag):
        super().__init__(mach, diag)
        self.tranTo = TranToFro(mach, diag, mach.nodeTerm, self, None, 0).reg()

    offMultiOk = NodeTo.offMultiOk_1

    def codePyFunMeat(self, logr):
        logr(f'raise TermStopException()')
    
    @g_logc.unredunKey
    def unredunKey(self):
        return (self.tranTo.to.uniq, 'Term')

#======================================================================================================================
# NodeCond

class NodeCond(NodeCodeMix, NodeToNset):
    def __init__(self, mach, diag):
        super().__init__(mach, diag)
        self.condNemptyEn = self.mach.scope.condNemptyEn
        self.tranByKeyD = {}

    def __getattr__(self, name):
        if None is not (ch := chtab.nameChD.get(name)):
            if ch in self.tranByKeyD:
                return self.tranByKeyD[ch].to
        raise AttributeError(self, name)
        
    def chainKey(self, key):
        if None is (tran := self.tranByKeyD.get(key)):
            node = NodeCond(self.mach, self.mach.diag0)
            tran = self.tranByKeyD[key] = TranToFroKey(self.mach, self.mach.diag0, node, self, key, 1).reg()
        return tran

    def chset(self):
        return objlib.ChsetObj(self.mach, self.mach.diag0, {k:None for k in self.tranByKeyD})
        
    def codePyFun(self, logr):
        with logr(f'def f{self.uniq}(self): #{self.iden()}'):
            logr(f'self.srcCh=self.srcA[self.src+{self.off}]')
            logr(f'g_logc.ch(self, {self.off}, self.srcCh)')
            logr(f'return Lut{self.uniq}.get(self.srcCh, f{self.tranTo.to.uniq}) #{self.tranTo.to.iden()}')

    def codePyLut(self, logr):
        with logr(f'Lut{self.uniq} = {{ #{self.iden()}'):
            for tran in self.tranByKeyD.values():
                logr(f'{repr(tran.key)}:f{tran.to.uniq}, #{tran.to.iden()}')
        logr(f'}}')

    def condNemptyP(self):
        return self.condNemptyEn and bool(self.tranByKeyD)
        
    def dumpNodeTreeFull(self, logr, pre, ind):
        self.dumpNodeTreeHead(logr, pre)
        with logr if ind else loglib.logNoop:
            accD = {}
            for tran in self.tranByKeyD.values():
                # todo make sure tran.off is consistent
                if None is (x := accD.get(tran.to.uniq)):
                    accD[tran.to.uniq] = [tran.to, [ tran.key ], tran]
                else:
                    x[1].append(tran.key)
                    if tran.prioDump() < x[2].prioDump():
                        x[2] = tran
            for x in accD.values():
                x[0].dumpNodeTree(logr, f'{dumpOff(x[2], 1)}{chtab.chsetDes(x[1])} ', 1, x[2])
            self.tranTo.to.dumpNodeTree(logr, dumpOff(self.tranTo, 0), 0, self.tranTo)

    def nodeByKey(self, key):
        return self.tranByKeyD[key].to

    def offMultiOk(self):
        return not self.tranByKeyD

    def removeFwd(self):
        super().removeFwd()
        for tran in self.tranByKeyD.values():
            tran.to.froTranRemove(tran)
        
    def offPropFwd(self):
        self.tranTo.offSet(self.offFwd)
        for tran in self.tranByKeyD.values():
            tran.offSet(self.offFwd)

    @g_logc.unredunKey
    def unredunKey(self):
        v = [self.tranTo.to.uniq]
        if self.tranByKeyD:
            v += ('Cond', self.off)
            for tran in self.tranByKeyD.values():
                v += (tran.key, tran.to.uniq)
        return tuple(v)
            
    def verify1(self):
        if OffMulti == self.off and self.tranByKeyD:
            self.mach.errN += 1
            g_logc.errNodeOffErr(self)
        super().verify1()
        for tran in self.tranByKeyD.values():
            tran.verify()

#======================================================================================================================
# NodeIf

class NodeIf(NodeCodeMix, NodeToNset):
    def __init__(self, mach, diag, exprObj):
        super().__init__(mach, diag)
        self.exprObj = exprObj
        self.tranThen = TranToFro(self.mach, diag, NodeCond(self.mach, diag), self, 'then', 0).reg()

    def codePyFun(self, logr):
        with logr(f'def f{self.uniq}(self): #{self.iden()}'):
            evalT,execT = self.exprObj.codePyEvalExecTexts()
            logr.ml(execT)
            with logr(f'if {evalT}:'):
                logr(f'return f{self.tranThen.to.uniq} #{self.tranThen.to.iden()}')
            logr(f'return f{self.tranTo.to.uniq} #{self.tranTo.to.iden()}')

    def desDumpNodeTree(self):
        return f'{self.des0()} [{self.off}] <{self.__class__.__name__}> {util.des0(self.exprObj)}'
    
    def dumpNodeTreeFull(self, logr, pre, ind):
        self.dumpNodeTreeHead(logr, pre)
        with logr if ind else loglib.logNoop:
            self.tranThen.to.dumpNodeTree(logr, f'{dumpOff(self.tranThen, 0)}[then] ', 1, self.tranThen)
            self.tranTo.to.dumpNodeTree(logr, dumpOff(self.tranTo, 0), 0, self.tranTo)

    def removeFwd(self):
        super().removeFwd()
        self.tranThen.to.froTranRemove(self.tranThen)
        
    offMultiOk = NodeTo.offMultiOk_1

    def offPropFwd(self):
        self.tranTo.offSet(self.offFwd)
        self.tranThen.offSet(self.offFwd)

    @g_logc.unredunKey
    def unredunKey(self):
        return (self.tranTo.to.uniq, 'If', self.exprObj.unredunKey(), self.tranThen.to.uniq)

    def verify1(self):
        super().verify1()
        self.tranThen.verify()

#======================================================================================================================
# NodeToOffDec

class NodeToOffDec(NodeToNset):
    def __init__(self, mach, diag, dec):
        super().__init__(mach, diag)
        self.dec = dec
        
    def desDumpNodeTree(self):
        return f'{self.des0()} [{self.off}] <{self.__class__.__name__}> dec={self.dec}'    

    def offPropModFwd(self):
        self.offFwd -= self.dec

    @g_logc.unredunKey
    def unredunKey(self):
        return (self.tranTo.to.uniq,)

#======================================================================================================================
# NodeToCall

class NodeToCall(NodeCodeMix, NodeToNset):
    def __init__(self, mach, diag, callObj):
        super().__init__(mach, diag)
        self.callObj = callObj

    def codePyFunMeat(self, logr):
        logr.ml(self.callObj.codePyExecText())
            
    def desDumpNodeTree(self):
        return f'{self.des0()} [{self.off}] <{self.__class__.__name__}> {util.des0(self.callObj)}'

    offMultiOk = NodeTo.offMultiOk_1
    
    def offSearchSrcAssignMatchP(self, searchr):
        return self.callObj.srcAssignSearchMatchP(searchr.target)

    @g_logc.unredunKey
    def unredunKey(self):
        return (self.tranTo.to.uniq, 'Call', self.callObj.unredunKey())

#======================================================================================================================
# NodeToCallSrcAssign

class NodeToCallSrcAssign(NodeToCall):
    def codePyFunMeat(self, logr):
        super().codePyFunMeat(logr)
        logr(f'self.linePopGt()')
        
    def offPropModFwd(self):
        self.offFwd = self.offSearchSrcAssign(self.callObj.argV[2])

#======================================================================================================================
# NodeToLineInc

class NodeToLineInc(NodeCodeMix, NodeToNset):
    def desDumpNodeTree(self):
        return f'{self.des0()} [{self.off}] <{self.__class__.__name__}> off={self.off}'

    def codePyFunMeat(self, logr):
        logr(f'self.lineInc({self.off!r})')
        
    @g_logc.unredunKey
    def unredunKey(self):
        return (self.tranTo.to.uniq, 'LineInc', self.off)

#======================================================================================================================
# NodeToSrcInc

class NodeToSrcIncBase(NodeCodeMix, NodeToNset):
    def codePyFunMeat(self, logr):
        logr(f'self.src+={self.inc}')

    def desDumpNodeTree(self):
        return f'{self.des0()} [{self.off}] <{self.__class__.__name__}> inc={self.inc}'
    
    @g_logc.unredunKey
    def unredunKey(self):
        return (self.tranTo.to.uniq, 'SrcInc', self.inc)

class NodeToSrcIncNarg(NodeToSrcIncBase):
    def __init__(self, mach, diag):
        super().__init__(mach, diag)
        self.inc = None

    def offPropModFwd(self):
        self.inc = self.off
        self.offFwd -= self.inc
        
class NodeToSrcIncArg(NodeToSrcIncBase):
    def __init__(self, mach, diag, inc):
        super().__init__(mach, diag)
        self.inc = inc

    def offPropModFwd(self):
        self.offFwd -= self.inc
    
class NodeToSrcIncFrom(NodeToSrcIncBase):
    def __init__(self, mach, diag, node0):
        super().__init__(mach, diag)
        self.inc = None
        self.node0 = node0
        
    def desDumpNodeTree(self):
        return f'{self.des0()} [{self.off}] <{self.__class__.__name__}> node0={util.des0(self.node0)} inc={self.inc}'
    
    def offPropModFwd(self):
        if OffNset == self.node0.off:
            raise StopOffNready()
        elif 0 > self.off or 0 > self.node0.off:
            self.mach.offErrDset[id(self)] = self
        else:
            self.inc = self.off - self.node0.off
            self.offFwd -= self.inc

#======================================================================================================================
# ChainHead ChainTerm
#======================================================================================================================

class ChainHeadObj(objlib.ObjBase):
    def chainTo(self, to):
        pass

    def chainToTopTran(self, tran):
        self.mach.topTranDset[id(tran)] = tran

class ChainTermObj(objlib.ObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        pass

class ChainTermInsertObj(ChainTermObj):
    def __init__(self, mach, diag, prev0, head):
        super().__init__(mach, diag)
        self.prev0 = prev0
        self.head = head
        self.prevV = []
        mach.insertObjV.append(self)
    
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        self.prevV.append(prev)

    def insertGo(self):
        with g_logc.insertGo(self):
            tail = self.prev0.to
            self.prev0.replaceTo(self.head)
            for prev in self.prevV:
                tran = prev.chainTo(tail)
                # copy prio1 for dumpNodeTree
                tran.prio1 = self.prev0.prio1

#======================================================================================================================
# Tran 
#======================================================================================================================

class FroTranFavNone:
    def idenAB(self, loopD):
        return ('<None>',0)
    
    def prioDump(self):
        return (3, TranPrioMax) 

    prioIden = prioDump
    
froTranFavNone = FroTranFavNone()

class TranToBase(objlib.ObjBase): #abstract
    def __init__(self, mach, diag, to):
        super().__init__(mach, diag)
        self.to = to
        #self.prio1

    def chainTo(self, to):
        raise TranChainToAlreadyException(self, to)
    
    def chainToSameTo(self, node):
        raise TranChainToAlreadyException(self, to)

    def chainToOk(self):
        return False
    
    def desPrio(self):
        return 'Max' if TranPrioMax == self.prio1 else self.prio1

    def desOff(self):
        return None

    def iden(self):
        return self.iden1({})

    def keyIs(self, key):
        return False

    def offSearchSrcAssignFro(self, searchr): pass

    def prioDump(self):
        return (1, self.prio1)

    prioIden = prioDump

    def reg(self):
        self.mach.tranPrio1I += 1
        self.prio1 = self.mach.tranPrio1I
        self.to.froTranAppend(self)
        return self

    def replaceTo(self, to):
        self.to.froTranRemove(self)
        self.to = to
        to.froTranAppend(self)
    
    def unredunRegFro(self): pass

    def verify(self):
        if self not in self.to.froTranV:
            raise TranVerifyException(self)
        self.to.verify()

class TranToIden(TranToBase):
    def __init__(self, mach, diag, to, idenX):
        super().__init__(mach, diag, to)
        self.idenX = idenX
        self.prioDumpX = 2
        
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        prev.chainToTopTran(self)
        self.to.chain(chainV, chainI, prev)

    def des0(self):
        return f'{self.desPrio()}__{self.iden()!r}__{util.desTyp(self.to)}'

    def desFro(self):
        return repr(self.iden)

    def iden1(self, loopD):
        return self.idenX
        
    def idenAB(self, loopD):
        return self.idenX,0
    
    def nodeByKey(self, key):
        return self.to.nodeByKey(key)

    def prioDump(self):
        return (self.prioDumpX, self.prio1)

    def prioIden(self):
        return (0, self.prio1)

class TranToFro(TranToBase):
    def __init__(self, mach, diag, to, fro, key, off):
        super().__init__(mach, diag, to)
        self.fro = fro
        self.key = key
        self.off = off
        
    def chainTranOffSet(self, off):
        self.off = off
    
    def des0(self):
        return f'{self.desPrio()}__{util.des0(self.fro)}__{self.desKey()}{self.off:+d}__{util.des0(self.to)}'

    def desFro(self):
        return self.fro.des0()

    def desKey(self):
        return '' if None is self.key else f'{self.key}'
    
    def desOff(self):
        return f'{self.fro.offFwd}+{self.off}'

    def iden1(self, loopD):
        a,b = self.idenAB(loopD)
        return f'{a}+{b}' if b else a
        
    def idenAB(self, loopD):
        if None is self.key:
            a,b = self.fro.idenAB(loopD)
            return a,b+1
        else:
            return f'{self.fro.iden1(loopD)}.{self.key}',0

    def offSearchSrcAssignFro(self, searchr):
        return self.fro.offSearchSrcAssign1(searchr)

    def offSet(self, offFwd):
        self.to.offSet(offFwd if 0 > offFwd else offFwd + self.off)

    def unredunRegFro(self):
        self.mach.unredunReg(self.fro)

class TranToFroNset(TranToFro):
    def reg(self):
        self.prio1 = TranPrioMax
        self.to.froTranAppend(self)
        return self

    def chainTo(self, to):
        g_logc.chainTo(self, to)
        self.__class__ = TranToFro
        self.to.froTranRemove(self)
        self.to = to
        self.reg()
        return self

    def chainToSameTo(self, node):
        self.off = node.tranTo.off
        return self.chainTo(node.tranTo.to)
    
    def chainToOk(self):
        return True

class TranToFroKey(TranToFro):
    def chainKey(self, key):
        return self.to.chainKey(key)

    def chainTo(self, to):
        return self.to.tranTo.chainTo(to)

    def chainToSameTo(self, node):
        return self.to.tranTo.chainToSameTo(node)

    def chainToOk(self):
        return self.to.tranTo.chainToOk()
    
    def desKey(self):
        return f'{self.key!r}'
        
    def idenAB(self, loopD):
        return f'{self.fro.iden1(loopD)}.{chtab.name1(self.key)}',0

    def keyIs(self, key):
        return key == self.key
