from __main__ import g_logc

import actlib
import chtab
#import codepylib
import funlib
import nodelib
import objlib
import scanlib
import util

from pylib0_xmzt import loglib

import collections
import functools
import itertools
import os
import re
import traceback

#======================================================================================================================
# exceptions
#======================================================================================================================

class ErrNException(Exception): pass #(errN)

#======================================================================================================================
# scope
#======================================================================================================================

class Scope:
    pass

def scopePop0(scope, mach):
    scope.mach = mach

    def set(k, f, *args): setattr(scope, k, f(mach, mach.diag0, *args))
    
    # basic
    set('None', objlib.VoidNoneObj)
    set('@', funlib.VoidRetFunObj)
    set('=', funlib.AssignFunObj, '=')
    for x in '+ - * / | & ^ << >> < <= == != >= >'.split():
        set(x, funlib.BinopFunObj, x)
    for x in '+= -= *= /= |= &= ^= <<= >>='.split():
        set(x, funlib.BinopAssignFunObj, x)
    set('list', funlib.ListFunObj)
    
    set('sym', objlib.RunSymFactoryObj)
    set('mem', objlib.RunMemSymFactoryObj)

    set('int', objlib.DtypObj, 'int')
    set('srcPtr', objlib.DtypObj, 'srcPtr')
    set('str', objlib.DtypObj, 'str')
    
    obj = getattr(scope, '*')
    obj.chain = actlib.TranOff1SymObj.chain.__get__(obj, obj.__class__)
    set('!', actlib.TranOff0SymObj)
    set('?', actlib.QmSymObj)
    
    def setAct(k, f): setattr(scope, k, objlib.CallFunObj(mach, mach.diag0, f))
    
    # acts
    setAct('for', actlib.ForActObj)
    setAct('insert', actlib.InsertActObj)
    setAct('if', actlib.IfActObj)
    setAct('line+', actlib.LineIncActObj)
    setAct('off=', actlib.OffAssignActObj)
    setAct('off-', actlib.OffDecActObj)
    setAct('sameTo', actlib.SameToActObj)
    setAct('src<-', actlib.SrcAssignActObj)
    setAct('src+', actlib.SrcIncActObj)
    setAct('src+from', actlib.SrcIncFromActObj)
    setAct('term', actlib.TermActObj)
    
    # standard
    set('src', objlib.RunMemSymObj, 'src', 'srcPtr', None)
    set('*src', objlib.RunSrcDerefFactoryObj)

AsObjTab = {
    float: objlib.FloatLitObj,
    int: objlib.IntLitObj,
    str: objlib.StrLitObj,
}

#======================================================================================================================
# Mach
#======================================================================================================================

class Mach:
    @classmethod
    def compilFromGram(cls, path, gramFun):
        self = cls(Scope())
        self.scopePop0()
        gramFun(self)
        self.phaseCompilFromGram(path)
        
    def __init__(self, scope):
        self.scope = scope
        #self.chainV
        self.codeGloDset = {}
        #self.condNemptyEn
        self.dtypD = {
            ('acc', 1): 'str',
            'bsuI': 'int',
            'srcCh':'str',
            
        }
        self.errN = 0
        self.insertObjV = []
        self.mark = 0
        self.nodeDset = {}
        self.nodeUniqI = 0
        self.offPropDset = {} # nodes that need offProp called on them after node.off set
        #self.offErrDset
        self.topTranDset = {}
        self.tranPrio1I = 0
        #self.verifyN

        self.diag0 = objlib.Diag0()
        self.voidObj = objlib.VoidObj(self, self.diag0)
        self.nodeNset = nodelib.NodeNset(self, self.diag0)
        self.nodeTerm = nodelib.NodeTerm(self, self.diag0)

    def asObj(self, x, diag):
        return x.asObj() if hasattr(x, 'asObj') else AsObjTab.get(type(x), objlib.ForeignObj)(self, diag, x)
    
    def codePy(self, logr):
        for node in self.nodeDset.values():
            node.codePyFun(logr)
        for node in self.nodeDset.values():
            node.codePyLut(logr)
        for tran in self.topTranDset.values():
            logr(f'{tran.to.iden()} = f{tran.to.uniq}')
                    
    def condNemptyV(self):
        return [node for node in self.nodeDset.values() if node.condNemptyP()]

    def dumpNodeTree(self, path):
        with open(path, 'w') as f:
            logr = loglib.Logr5File(f)
            self.mark += 1
            self.nodeNset.mark = self.mark
            self.nodeTerm.mark = self.mark
            # dump topTranDset first
            for tran in self.topTranDset.values():
                if tran.to.mark != self.mark:
                    tran.to.mark = self.mark
                    tran.to.dumpNodeTreeFull(logr, '', 1)
            for node in self.nodeDset.values():
                if node.mark != self.mark:
                    tran.to.mark = self.mark
                    node.dumpNodeTreeFull(logr, '[?] ', 1)

    def parse(self, src, srcA=0):
        # todo try to inspect source position of text for diagnostics 
        self.chainV = []
        scanlib.Scanr(self, self.parseObj, src, srcA).go()
        
    def parseObj(self, obj):
        with g_logc.parseObj(obj):
            obj.parseObjGo()

    def parseObjAcc(self, obj):
        self.chainV.append(obj)

    def parseObjEol(self, obj):
        if self.chainV:
            with g_logc.chainGo(self.chainV):
                # terminate chain
                self.chainV.append(nodelib.ChainTermObj(self, obj.diag))
                # initialize per-chain variables
                self.scope.condNemptyEn = 1
                # chain go
                self.chainV[0].chain(self.chainV, 1, nodelib.ChainHeadObj(self, obj.diag))
                g_logc.dumpNodeTreeChain(self)
                # reset for next chain 
                self.chainV = []
                
    def scopePop0(self):
        scopePop0(self.scope, self)
        g_logc.scopeDump0(self.scope)
        
    def unredunReg(self, node):
        self.unredunQ[id(node)] = node

    def verify(self):
        self.verifyN = 0
        self.mark += 1
        for tran in self.topTranDset.values():
            tran.to.verify()
        return self.verifyN

    #--------------------------------------------------------------------------------------------------------------------
    # phase
        
    def phaseCompilFromGram(self, path):
        self.phaseGram()
        self.phaseInsert()
        self.phaseOff()
        self.phaseCheck()
        self.phaseUnredun()
        self.phaseCompil(path)

    def phaseFin(self):
        g_logc.phaseStat(self)
        g_logc.dumpNodeTreePhase(self)
        if self.errN:
            raise ErrNException(self.errN)

    def phaseGram(self):
        with g_logc.phaseGo('gram'):
            self.phaseFin()
        
    def phaseInsert(self):
        with g_logc.phaseGo('insert'):
            for obj in self.insertObjV:
                obj.insertGo()
            self.phaseFin()

    def phaseOff(self):
        with g_logc.phaseGo('offProp'):
            self.offErrDset = {}
            while self.offPropDset:
                propDset = self.offPropDset
                g_logc.offPropIter(propDset)
                self.offPropDset = {}
                for node in propDset.values():
                    node.offProp()
            # check for off unset
            for node in self.nodeDset.values():
                if nodelib.OffNset == node.off:
                    self.offErrDset[id(node)] = node
            # dump accumulated errors
            for node in self.offErrDset.values():
                self.errN += 1
                g_logc.errNodeOff(node)
            self.phaseFin()

    def phaseCheck(self):
        with g_logc.phaseGo('check'):
            for tran in self.nodeNset.froTranV:
                self.errN += 1
                g_logc.errMachTranNset(tran)
            if not self.nodeTerm.froTranV:
                self.errN += 1
                g_logc.errMachNterm()
            self.phaseFin()

    def phaseUnredun(self):
        with g_logc.phaseGo('unredun'):
            self.unredunD = {} # value is (node,replable). 
            self.unredunQ = {}

            # init d with identity replacements.
            # these identity replacements are not further replable.
            # all future replacements will be replable.
            for node in self.nodeDset.values():
                self.unredunD[node.unredunKey0()] = (node,0)
                self.unredunQ[id(node)] = node

            replN = 0
            while self.unredunQ:
                key,node = self.unredunQ.popitem()
                k = node.unredunKey()
                if None is (x := self.unredunD.get(k)):
                    self.unredunD[k] = (node,1)
                else:
                    repl,replable = x
                    if node is not repl:
                        if replable and node.uniq < repl.uniq:
                            self.unredunD[k] = (node,1)
                            node,repl = repl,node
                    
                        replN += 1
                        g_logc.unredunRepl(node, repl, k)
                        for tran in node.replace(repl):
                            tran.unredunRegFro()
                        del self.nodeDset[id(node)]

            g_logc.unredunStat(self, replN)
            self.phaseFin()
        
    def phaseCompil(self, path):
        with g_logc.phaseGo(f'compil {path!r}'):
            with open(path, 'w') as f:
                logr = loglib.Logr5File(f)
                self.codePy(logr)
            self.phaseFin()
