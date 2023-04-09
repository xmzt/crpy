import util

from pylib0_xmzt import loglib

import itertools
import os

# main sets g_logc

#======================================================================================================================
# Logc
#======================================================================================================================

class Logc(loglib.Logc, metaclass=loglib.LogcMeta):
    def errMachNterm__1(self):
        return self.logr(f'[ERROR] MachNterm')
    
    def errMachTranNset__1(self, tran):
        return self.logr(f'[ERROR] MachTranNset {util.desTyp(tran)}')
    
    def errNodeOff__1(self, node):
        with self.logr(f'[ERROR] NodeOff {util.desTyp(node)} .off={node.off!r} .offFwd={node.offFwd!r}'):
            for tran in node.froTranV:
                self.logr(f'{util.des0(tran)} {tran.desOff()}')
            return self.logr
    
    def chainGo__1(self, chainV):
        with self.logr(f'[chainGo]'):
            for obj in chainV:
                self.logr(util.desTyp(obj))
            return self.logr
    
    def chainDumpNodeTree__1(self, mach):
        path = self.dumpNodeTreePath()
        with self.logr(f'[chainDumpNodeTree] {path}'):
            mach.dumpNodeTree(path)
            return self.logr

    def chainObj__0(self, f0): return f0
        
    def chainObj__1(self, f0):
        def f1(obj, chainV, chainI, prev):
            with self.logr(f'[chainObj] {chainI=!r} {util.desTyp(obj)}'):
                self.logr(f'prev: {util.desTyp(prev)}') 
                return f0(obj, chainV, chainI, prev)
        return f1

    def chainTo__1(self, tran, to):
        with self.logr(f'[chainTo] {util.desTyp(tran)}'):
            return self.logr(f'to: {util.desTyp(to)}')

    def codePyCast__1(self, x, dstDtyp, srcDtyp):
        return self.logr(f'[codePyCast] {x!r} {dstDtyp=} {srcDtyp=}')
    
    dumpNodeTreeFro = 0

    def dumpNodeTreeChain__1(self, mach):
        return self.dumpNodeTreeGo(mach, '[dumpNodeTreeChain] ')

    def dumpNodeTreeInit(self, pathBase):
        self.dumpNodeTreePathBase = pathBase
        for i in itertools.count(0):
            try:
                os.remove(f'{self.dumpNodeTreePathBase}{i}')
            except FileNotFoundError:
                break
        self.dumpNodeTreeI = -1
        return self
        
    def dumpNodeTreeGo(self, mach, pre):
        path = self.dumpNodeTreePath()
        with self.logr(f'{pre}{path}'):
            mach.dumpNodeTree(path)
            return self.logr
    
    def dumpNodeTreePath(self):
        self.dumpNodeTreeI += 1
        return f'{self.dumpNodeTreePathBase}{self.dumpNodeTreeI}'
    
    def dumpNodeTreePhase__1(self, mach):
        return self.dumpNodeTreeGo(mach, '[dumpNodeTreePhase] ')

    def evaObj__0(self, f0): return f0
        
    def evaObj__1(self, f0):
        def f1(obj, spec):
            with self.logr(f'[evaObj] {util.desTyp(obj)} {spec=}'):
                res = f0(obj, spec)
                self.logr(f'res: {util.desTyp(res)}')
                return res
        return f1

    def evaObjLst__0(self, f0): return f0
        
    def evaObjLst__1(self, f0):
        def f1(obj, spec, lst):
            with self.logr(f'[evaObjLst] {util.desTyp(obj)} {spec=}'):
                self.logr(f'lst: {util.des0(lst)}')
                res = f0(obj, spec, lst)
                self.logr(f'res: {util.desTyp(res)}')
                return res
        return f1

    def insertGo__1(self, obj):
        with self.logr(f'[insertGo] {util.desTyp(obj)}'):
            self.logr(f'prev0: {util.desTyp(obj.prev0)}')
            return self.logr(f'head: {util.desTyp(obj.head)}')

    def offPropIter__1(self, propDset):
        return self.logr(f'[offPropIter] dsetN={len(propDset)}')

    def offSet__1(self, node):
        return self.logr(f'[offSet] {util.desTyp(node)} off={node.off!r}')
    
    def offSearchSrcAssign0__1(self, searchr):
        return self.logr(f'[offSearchSrcAssign0] {util.desTyp(searchr.node0)} target={searchr.target}')
    
    def offSearchSrcAssign1__1(self, node, match):
        return self.logr(f'[offSearchSrcAssign1]{" MATCH" if match else ""} {util.desTyp(node)} off={node.off}')
        
    def offSearchSrcAssignRes__1(self, searchr):
        return self.logr(f'[offSearchSrcAssignRes] off={searchr.off}')
    
    def parseObj__1(self, obj):
        return self.logr(f'[parseObj] {util.desTyp(obj)}')

    def phaseGo__1(self, text):
        return self.logr(f'[phaseGo] {text}')

    def phaseStat__1(self, mach):
        return self.logr(f'[phaseStat] errN={mach.errN} nodeDsetN={len(mach.nodeDset)} verifyN={mach.verify()}')
    
    def scanChIn__1(self, scanr):
        return self.logr(f'[scanChIn] {scanr.srcPos(scanr.srcA)} srcCh={scanr.srcCh!r}')
    
    def scanObj__1(self, obj):
        return self.logr(f'[scanObj] {util.desTyp(obj)}')

    def scanRoot__1(self, root):
        with self.logr(f'[scanRoot]'):
            for obj in root.argV:
                self.logr(util.desTyp(obj))
            return self.logr

    def scanStack__1(self, scanr, inc):
        return self.logr(f'[scanStack] {scanr.srcPos(scanr.srcA)} {scanr.srcCh!r} n={len(scanr.stack)}{inc:+d}')

    def scanState__1(self, scanr, state):
        return self.logr(f'[scanState] {scanr.srcPos(scanr.srcA)} state={state!r}')

    def scopeDump0__1(self, scope):
        return scopeDump(scope, self.logr, '[scopeDump0]')

    def unredunKey__0(self, f0): return f0
        
    def unredunKey__1(self, f0):
        def f1(obj):
            with self.logr(f'[unredunKey] {util.desTyp(obj)}'):
                key = f0(obj)
                self.logr(f'key: {key!r}')
                return key
        return f1

    def unredunRepl__1(self, node, repl, k):
        with self.logr(f'[unredunRepl] {util.desTyp(node)}'):
            self.logr(f'repl: {util.desTyp(repl)}')
            return self.logr(f'key: {k!r}')

    def unredunStat__1(self, mach, replN):
        return self.logr(f'[unredunStat] qN={len(mach.unredunQ)} nodeDsetN={len(mach.nodeDset)} {replN=}')

def scopeDump(scope, logr, pre):
    with logr(pre):
        for k,v in scope.__dict__.items():
            logr(f'{k}: {util.desTyp(v)}')
        return logr
