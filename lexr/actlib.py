import funlib
import logclib
import nodelib
import objlib

import functools

from __main__ import g_logc

#======================================================================================================================
# helpers
#======================================================================================================================

def reduceOrRunP(a, b): return a & b.runP()

#------------------------------------------------------------------------------------------------------------------------
# ForActObj

class ForActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 3 != len(self.argV):
            raise objlib.ArgNException(self)
        dst = self.argV[1].eva(objlib.Spec.St)
        for x in self.argV[2].eva(objlib.Spec.Ld).asList():
            dst.evaAssign(x)
            self.mach.asObj(x, self.diag).chain(chainV, chainI, prev)

#------------------------------------------------------------------------------------------------------------------------
# IfActObj

class IfActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 3 > len(self.argV):
            raise objlib.ArgNException(self)
        prev.chainTo(node := nodelib.NodeIf(self.mach, self.diag, self.argV[1].eva(objlib.Spec.Ld)))
        thenChainV = self.argV[2:]
        thenChainV.append(nodelib.ChainTermObj(self.mach, self.diag))
        thenChainV[0].chain(thenChainV, 1, node.tranThen.to)
        chainV[chainI].chain(chainV, chainI+1, node)

#------------------------------------------------------------------------------------------------------------------------
# InsertActObj

class InsertActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 1 != len(self.argV):
            raise objlib.ArgNException(self)
        # create head node and chain to that
        head = nodelib.NodeCond(self.mach, self.diag)
        chainV[-1] = nodelib.ChainTermInsertObj(self.mach, self.diag)
        chainV[chainI].chain(chainV, chainI+1, head)

        tail = prev.to
        prev.replaceTo(head)
        for termPrev in chainV[-1].prevV:
            tran = termPrev.chainTo(tail)
            # copy prio1 for dumpNodeTree
            tran.prio1 = prev.prio1

#------------------------------------------------------------------------------------------------------------------------
# LineIncActObj
    
class LineIncActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 1 != len(self.argV):
            raise objlib.ArgNException(self)
        prev.chainTo(node := nodelib.NodeToLineInc(self.mach, self.diag))
        chainV[chainI].chain(chainV, chainI+1, node)

#------------------------------------------------------------------------------------------------------------------------
# Off*
    
class OffAssignActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 2 != len(self.argV):
            raise objlib.ArgNException(self)
        prev.offSet(self.argV[1].eva(objlib.Spec.Ld).asInt())
        chainV[chainI].chain(chainV, chainI+1, prev)

class OffDecActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 2 != len(self.argV):
            raise objlib.ArgNException(self)
        prev.chainTo(node := nodelib.NodeToOffDec(self.mach, self.diag, self.argV[1].eva(objlib.Spec.Ld).asInt()))
        chainV[chainI].chain(chainV, chainI+1, node)

#------------------------------------------------------------------------------------------------------------------------
# SameToActObj

class SameToActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 2 != len(self.argV):
            raise objlib.ArgNException(self)
        prev.chainToSameTo(node := self.argV[1].eva(objlib.Spec.Ld).asNode())
        chainV[chainI].chain(chainV, chainI+1, node)

#------------------------------------------------------------------------------------------------------------------------
# Src*ActObj

class SrcAssignActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 2 != len(self.argV):
            raise objlib.ArgNException(self)
        callArgV = [getattr(self.mach.scope, '='), self.mach.scope.src, self.argV[1].eva(objlib.Spec.Ld)]
        callObj = funlib.AssignRunObj(self.mach, self.diag, callArgV)
        prev.chainTo(node := nodelib.NodeToCallSrcAssign(self.mach, self.diag, callObj))
        chainV[chainI].chain(chainV, chainI+1, node)

class SrcIncActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 1 == len(self.argV):
            prev.chainTo(node := nodelib.NodeToSrcIncNarg(self.mach, self.diag))
        elif 2 == len(self.argV):
            node = nodelib.NodeToSrcIncArg(self.mach, self.diag, self.argV[1].eva(objlib.Spec.Ld).asInt())
            prev.chainTo(node)
        else:
            raise objlib.ArgNException(self)
        chainV[chainI].chain(chainV, chainI+1, node)

class SrcIncFromActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 2 != len(self.argV):
            raise objlib.ArgNException(self)
        node0 = self.argV[1].eva(objlib.Spec.Ld).asNode()
        prev.chainTo(node := nodelib.NodeToSrcIncFrom(self.mach, self.diag, node0))
        chainV[chainI].chain(chainV, chainI+1, node)
    
#------------------------------------------------------------------------------------------------------------------------
# TranOff Qm

class TranOff0SymObj(objlib.ObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        prev.chainTranOffSet(0)
        chainV[chainI].chain(chainV, chainI+1, prev)

class TranOff1SymObj(objlib.ObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        prev.chainTranOffSet(1)
        chainV[chainI].chain(chainV, chainI+1, prev)

class QmSymObj(objlib.ObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if prev.chainToOk():
            chainV[chainI].chain(chainV, chainI+1, prev)

#------------------------------------------------------------------------------------------------------------------------
# TermActObj

class TermActObj(objlib.CallObjBase):
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        if 1 != len(self.argV):
            raise objlib.ArgNException(self)
        prev.chainTo(node := nodelib.NodeToTerm(self.mach, self.diag))
        chainV[chainI].chain(chainV, chainI+1, node)
