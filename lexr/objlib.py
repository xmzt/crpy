from __main__ import g_logc

import chtab
import codepylib
import logclib
import nodelib
import util

from pylib0_xmzt import enulib

import ast
import functools
import re
import sys

#======================================================================================================================
# constants
#======================================================================================================================

Spec = enulib.EnuBitmap.create('Spec').addV('Ld St'.split())

class ArgNException(Exception): pass #(obj)
class LdNexistException(Exception): pass
class StNvalidException(Exception): pass

#======================================================================================================================
# Diag: diagnostic info (to print location in source code and code fragment)
#
# use mach.diag0 singleton rather than Diag0()
#======================================================================================================================

class Diag0:
    def srcPos(self):
        return '-.-/-'
        
    def srcText(self):
        return ''

class DiagScanr:
    def __init__(self, scanr, srcA, srcE):
        self.scanr = scanr
        self.srcA = srcA
        self.srcE = srcE
    
    def srcPos(self):
        return self.scanr.srcPos(self.srcA)
        
    def srcText(self):
        return self.scanr.src[self.srcA:self.srcE]

class DiagDeri:
    def __init__(self, srcObj):
        self.srcObj = srcObj
        
    def srcPos(self):
        return self.srcObj.srcPos()
        
    def srcText(self):
        return self.srcObj.srcText()

#======================================================================================================================
# ObjBase: abstract, all objects derive from this
#======================================================================================================================

class ObjBase:
    def __init__(self, mach, diag):
        self.mach = mach
        self.diag = diag

    def asObj(self):
        return self

    #def asDtypS(self)
    #def asInt(self)
    #def asList(self)
    #def asSymS(self)

    def chainToTopTran(self, tran): pass

    def des0(self):
        return self.__class__.__name__
        
    def desTyp(self):
        return f'<{self.__class__.__name__}>{self.des0()}'

    def desTypSrc(self):
        return f'<{self.__class__.__name__} {self.diag.srcPos()} {self.diag.srcText()}>{self.des0()}'

    __repr__ = desTypSrc
    
    def dtyp(self):
        return None
    
    def dtypArg(self, i):
        return None
    
    @g_logc.evaObj
    def eva_Ld(self, spec):
        if Spec.St & spec:
            raise StNvalidException(self)
        return self

    @g_logc.evaObj
    def eva_Ld_St(self, spec):
        return self
    
    eva = eva_Ld

    def offPropObj(self, off): pass

    def parseObjGo(self):
        self.mach.parseObjAcc(self)

    def srcAssignSearchMatchP(self, target):
        return False

    #def codePy(self, coder)
    
    def codePyEvalExecTexts(self):
        coder = codepylib.Coder()
        expr = self.codePy(coder)
        return expr, coder.evalExecText()

    def codePyExecText(self):
        coder = codepylib.Coder()
        return coder.execExecText(self.codePy(coder))

    def runP(self):
        return False

    def runP_1(self):
        return True

#======================================================================================================================
# Bare
#======================================================================================================================

class BareObj(ObjBase):
    def __init__(self, mach, diag, bare):
        super().__init__(mach, diag)
        self.bare = bare

    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        self.eva(Spec.Ld | Spec.St).chain(chainV, chainI, prev)

    def des0(self):
        return self.bare

    @g_logc.evaObj
    def eva(self, spec):
        segV = self.bare.split('.')
        root = self.mach.scope
        for i in range(0, len(segV) - 1):
            x = getattr(root, segV[i])
            # hook for run-time objects, maybe others?
            if hasattr(x, 'evaLookup'):
                return x.evaLookup(spec, segV[i+1:], self.diag)
            root = x

        # last segment
        try:
            x = getattr(root, segV[-1])
        except:
            pass
        else:
            if hasattr(x, 'evaLookup'):
                return x.evaLookup(spec, [], self.diag)
            elif Spec.Ld & spec:
                return self.mach.asObj(x, self.diag)
            elif Spec.St & spec:
                return SymObj(self.mach, self.diag, root, segV[-1], self.bare)
        # getattr failed
        if Spec.St & spec:
            return SymObj(self.mach, self.diag, root, segV[-1], self.bare)
        raise LdNexistException(self)

#======================================================================================================================
# CallObj
#
# todo: refactor common with LstObj 
#======================================================================================================================

class CallObjBase(ObjBase):
    def __init__(self, mach, diag, argV):
        super().__init__(mach, diag)
        self.argV = argV

    def des0(self):
        return util.desCall(self.argV)

class CallFunObj(ObjBase):
    def __init__(self, mach, diag, con):
        super().__init__(mach, diag)
        self.con = con

    @g_logc.evaLst
    def evaLst(self, spec, lst):
        return self.con(self.mach, lst.diag, lst.argV)
    
#======================================================================================================================
# Chset
#======================================================================================================================

class ChsetObj(ObjBase):
    def __init__(self, mach, diag, chDset):
        super().__init__(mach, diag)
        self.chDset = chDset
    
    def __iadd__(self, other):
        chtab.chsetIadd(self.chDset, other.chDset)
        return self

    def __isub__(self, other):
        chtab.chsetIsub(self.chDset, other.chDset)
        return self

    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        for ch in self.chDset:
            chainV[chainI].chain(chainV, chainI+1, prev.chainKey(ch))
        
    def des0(self):
        return chtab.chsetDes(self.chDset)

    def evaBinop(self, op, b, diag):
        # some fine hacky trickeration here if i do say so
        a = ChsetObj(self.mach, diag, self.chDset.copy())
        exec(f'a{op}=b')
        return a

    def evaBinopAssign(self, op, b):
        exec(f'self{op}b')
        return self

#======================================================================================================================
# Dtyp
#======================================================================================================================

class DtypObj(ObjBase):
    def __init__(self, mach, diag, dtypS):
        super().__init__(mach, diag)
        self.dtypS = dtypS

    def asDtypS(self):
        return self.dtypS

    def des0(self):
        return self.dtypS

#======================================================================================================================
# Eol
#======================================================================================================================

class EofObj(ObjBase):
    def parseObjGo(self):
        self.mach.parseObjEol(self)

class EolObj(ObjBase):
    def parseObjGo(self):
        self.mach.parseObjEol(self)

#======================================================================================================================
# Foreign
#======================================================================================================================

class ForeignObj(ObjBase):
    def __init__(self, mach, diag, val):
        super().__init__(mach, diag)
        self.val = val

    def asInt(self):
        return int(self.val)

    def asList(self):
        return self.val
        
    def des0(self):
        return repr(self.val)

    def evaBinop(self, op, b, diag):
        return self.mach.asObj(eval(f'self.val{op}b'), diag)

    def evaBinopAssign(self, op, b):
        exec(f'self.val{op}b')
        return self

    @g_logc.evaLst
    def evaLst(self, spec, lst):
        argV = [arg.eva(Spec.Ld) for arg in lst.argV[1:]]
        x = self.val(*argV)
        return self.mach.asObj(x, lst.diag)

#======================================================================================================================
# Lit
#======================================================================================================================

class LitObjBase(ObjBase):
    #LitType
    
    def __new__(cls, mach, diag, val):
        return cls.LitType.__new__(cls, val)

    def __init__(self, mach, diag, val):
        super().__init__(mach, diag)
    
    def codePy(self, coder):
        return self.LitType.__repr__(self)
    
    def des0(self):
        return self.LitType.__repr__(self)

    def dtyp(self):
        return self.LitType.__name__

    def evaBinop(self, op, b, diag):
        return self.mach.asObj(eval(f'self{op}b'), diag)

    @g_logc.unredunKey
    def unredunKey(self):
        return (self.LitType.__repr__(self),)
    
class FloatLitObj(LitObjBase, float):
    LitType = float
    
class IntLitObj(LitObjBase, int):
    LitType = int
    
    def asInt(self):
        return int(self)
    
class StrLitObj(LitObjBase, str):
    LitType = str
    
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        for ch in self:
            prev = prev.chainKey(ch)
        chainV[chainI].chain(chainV, chainI+1, prev)
        
#======================================================================================================================
# Lst
#======================================================================================================================

class LstObj(ObjBase):
    def __init__(self, mach, diag, argV):
        super().__init__(mach, diag)
        self.argV = argV

    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        return self.eva(Spec.Ld).chain(chainV, chainI, prev)

    def des0(self):
        return util.desCall(self.argV)
    
    @g_logc.evaObj
    def eva(self, spec):
        return self.argV[0].eva(Spec.Ld).evaLst(spec, self)
    
    def scanAcc(self, x):
        self.argV.append(x)

#======================================================================================================================
# VoidObj
#======================================================================================================================

class VoidObj(ObjBase):
    def asDtypS(self):
        return None
    
    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        chainV[chainI].chain(chainV, chainI+1, prev)
        
class VoidNoneObj(ObjBase):
    @g_logc.evaLookup
    def evaLookup(self, spec, segV, diag):
        return RunDotObj(self.mach, diag, self.mach.voidObj, segV) if segV else self.mach.voidObj
        
#======================================================================================================================
# Sym
#======================================================================================================================

class SymObj(ObjBase):
    def __init__(self, mach, diag, root, attr, bare):
        super().__init__(mach, diag)
        self.root = root
        self.attr = attr
        self.bare = bare

    def asSymS(self):
        return self.bare

    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        node = nodelib.NodeCond(self.mach, self.diag)
        tran = nodelib.TranToIden(self.mach, self.diag, node, self.bare).reg()
        self.evaAssign(tran)
        tran.chain(chainV, chainI, prev)

    def codePy(self, coder):
        return self.bare

    def des0(self):
        return self.bare

    def evaAssign(self, b):
        exec(f'self.root.{self.attr}=b')
        return b

#======================================================================================================================
# Run*
#======================================================================================================================

class RunObjBase(ObjBase):
    runP = ObjBase.runP_1

class RunCallObj(ObjBase):
    def __init__(self, mach, diag, argV):
        super().__init__(mach, diag)
        self.argV = argV

    @g_logc.chainObj
    def chain(self, chainV, chainI, prev):
        prev.chainTo(node := nodelib.NodeToCall(self.mach, self.diag, self))
        chainV[chainI].chain(chainV, chainI+1, node)

    def codePy(self, coder):
        v = []
        for i in range(1, len(self.argV)):
            arg = self.argV[i]
            v.append(coder.cast(arg.codePy(coder), self.argV[0].dtypArg(i), arg.dtyp()))
        return coder.hang(f"{self.argV[0].codePy(coder)}({','.join(v)})")
        
    def des0(self):
        return util.desCall(self.argV)

    def offPropObj(self, off):
        for arg in self.argV:
            arg.offPropObj(off)

    @g_logc.unredunKey
    def unredunKey(self):
        return tuple([arg.unredunKey() for arg in self.argV])
    
class RunDotObj(RunObjBase):
    def __init__(self, mach, diag, root, segV):
        super().__init__(mach, diag)
        self.root = root
        self.segV = segV

    def codePy(self, coder):
        return '.'.join([self.root.codePy(coder)] + self.segV)

    def des0(self):
        return '.'.join([self.root.des0()] + self.segV)

    def offPropObj(self, off):
        self.root.offPropObj(off)

    @g_logc.unredunKey
    def unredunKey(self):
        return tuple(['.', self.root.unredunKey()] + self.segV)
    
class RunSymObj(RunObjBase):
    def __init__(self, mach, diag, bare, dtypX, dtypArgV):
        super().__init__(mach, diag)
        self.bare = bare
        self.dtypX = dtypX
        self.dtypArgV = dtypArgV

    def codePy(self, coder):
        return self.bare

    def des0(self):
        return self.bare if None is self.dtypX and not self.dtypArgV else f'({self.bare},{self.dtypX},{self.dtypArgV})'

    def dtyp(self):
        return self.dtypX

    def dtypArg(self, i):
        try:
            return self.dtypArgV[i]
        except:
            return None
    
    @g_logc.evaLookup
    def evaLookup(self, spec, segV, diag):
        return RunDotObj(self.mach, diag, self, segV) if segV else self

    def evaLst(self, spec, lst):
        return RunCallObj(self.mach, lst.diag, [self] + [arg.eva(Spec.Ld) for arg in lst.argV[1:]])
        
    @g_logc.unredunKey
    def unredunKey(self):
        return (self.bare,)
    
class RunSymFactoryObj(ObjBase):
    InstanceClas = RunSymObj

    @g_logc.evaLst
    def evaLst(self, spec, lst):
        if 2 > len(lst.argV):
            raise ArgNException(self)
        sym = lst.argV[1].eva(Spec.St)
        dtyp = None
        dtypArgV = None
        if 2 < len(lst.argV):
            dtyp = lst.argV[2].eva(Spec.Ld).asDtypS()
            if 3 < len(lst.argV):
                dtypArgV = [arg.eva(Spec.Ld).asDtypS() for arg in lst.argV[3:]]
        obj = self.InstanceClas(self.mach, lst.diag, sym.asSymS(), dtyp, dtypArgV)
        sym.evaAssign(obj)
        return obj

class RunMemSymObj(RunSymObj):
    def codePy(self, coder):
        return f'self.{self.bare}'

class RunMemSymFactoryObj(RunSymFactoryObj):
    InstanceClas = RunMemSymObj

class RunSrcDerefObj(RunObjBase):
    def __init__(self, mach, diag):
        super().__init__(mach, diag)
        self.off = None
        
    def codePy(self, coder):
        return f'self.srcA[self.src+{self.off}]'

    def des0(self):
        return f'(*src off={self.off})'

    def dtyp(self):
        return 'str'
        
    def offPropObj(self, off):
        self.off = off - 1

    @g_logc.unredunKey
    def unredunKey(self):
        return ('*src',)

class RunSrcDerefFactoryObj(ObjBase):
    @g_logc.evaLookup
    def evaLookup(self, spec, segV, diag):
        obj = RunSrcDerefObj(self.mach, diag)
        return RunDotObj(self.mach, diag, obj, segV) if segV else obj

