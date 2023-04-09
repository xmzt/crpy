from __main__ import g_logc

import logclib
import nodelib
import objlib
import util

import functools

#======================================================================================================================
# OpFunObj
#======================================================================================================================

class OpFunObj(objlib.ObjBase):
    def __init__(self, mach, diag, op):
        super().__init__(mach, diag)
        self.op = op

    def des0(self):
        return self.op

    @g_logc.unredunKey
    def unredunKey(self):
        return (self.op,)
    
#======================================================================================================================
# Binop
#======================================================================================================================

class BinopFunObj(OpFunObj):
    @g_logc.evaLst
    def evaLst(self, spec, lst):
        if 3 > len(lst.argV):
            raise objlib.ArgNException(lst)
        argV = [self]
        runP = 0 
        for arg in lst.argV[1:]:
            argV.append(arg := arg.eva(objlib.Spec.Ld))
            runP |= arg.runP()
        if runP:
            return BinopRunObj(self.mach, lst.diag, argV)

        # eval comp-time
        a = argV[1]
        for b in argV[2:]:
            a = a.evaBinop(self.op, b, lst.diag)
        return a

class BinopRunObj(objlib.RunCallObj):
    def codePy(self, coder):
        a = self.argV[1].codePy(coder)
        aDtyp = self.argV[1].dtyp()
        for b in self.argV[2:]:
            a = f'{a}{self.argV[0].op}{coder.cast(b.codePy(coder), aDtyp, b.dtyp())}'
        return coder.hang(a)

#======================================================================================================================
# BinopAssign
#======================================================================================================================

class BinopAssignFunObj(OpFunObj):
    @g_logc.evaLst
    def evaLst(self, spec, lst):
        if 3 > len(lst.argV):
            raise objlib.ArgNException(lst)
        argV = [self, (arg := lst.argV[1].eva(objlib.Spec.St))]
        runP = arg.runP()
        for arg in lst.argV[2:]:
            argV.append(arg := arg.eva(objlib.Spec.Ld))
            runP |= arg.runP()
        if runP:
            return BinopAssignRunObj(self.mach, lst.diag, argV)

        # eval comp-time
        a = argV[1]
        for b in argV[2:]:
            a.evaBinopAssign(self.op, b)
        return a

class BinopAssignRunObj(objlib.RunCallObj):
    def codePy(self, coder):
        a = self.argV[1].codePy(coder)
        aDtyp = self.argV[1].dtyp()
        for b in self.argV[2:]:
            coder.acc(f'{a}{self.argV[0].op}{coder.cast(b.codePy(coder), aDtyp, b.dtyp())}')
        return coder.nhang(a)
        
#======================================================================================================================
# Assign
#======================================================================================================================

class AssignFunObj(OpFunObj):
    @g_logc.evaLst
    def evaLst(self, spec, lst):
        if 3 > len(lst.argV):
            raise objlib.ArgNException(lst)
        argV = [self]
        runP = 0
        for arg in lst.argV[1:-1]:
            argV.append(arg := arg.eva(objlib.Spec.St))
            runP |= arg.runP()
        argV.append(arg := lst.argV[-1].eva(objlib.Spec.Ld))
        runP |= arg.runP()
        if runP:
            return AssignRunObj(self.mach, lst.diag, argV)

        # eval comp-time
        b = argV[-1]
        for a in reversed(argV[1:-1]):
            a.evaAssign(b)
        return b
        
class AssignRunObj(objlib.RunCallObj):
    def codePy(self, coder):
        b = self.argV[-1].codePy(coder)
        bDtyp = self.argV[-1].dtyp()
        for a in reversed(self.argV[1:-1]):
            coder.acc(f'{a.codePy(coder)}{self.argV[0].op}{coder.cast(b, a.dtyp(), bDtyp)}')
        return coder.nhang(b)

    def srcAssignSearchMatchP(self, target):
        return (self.mach.scope.src is self.argV[-1] and target in self.argV[:-1])

#======================================================================================================================
# List
#======================================================================================================================

class ListFunObj(objlib.ObjBase):
    @g_logc.evaLst
    def evaLst(self, spec, lst):
        argV = [arg.eva(objlib.Spec.Ld) for arg in lst.argV[1:]]
        return objlib.ForeignObj(self.mach, lst.diag, argV)
        
#======================================================================================================================
# VoidRet
#======================================================================================================================

class VoidRetFunObj(objlib.ObjBase):
    @g_logc.evaLst
    def evaLst(self, spec, lst):
        if 2 > len(lst.argV):
            raise objlib.ArgNException(lst)
        lst.argV[1].eva(objlib.Spec.Ld).evaLst(spec, objlib.LstObj(self.mach, lst.diag, lst.argV[1:]))
        return self.mach.voidObj
