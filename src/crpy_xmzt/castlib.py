from pylib0_xmzt.denumlib import Denum

class CastException(Exception): pass
class FlagsUnexpectedException(CastException): pass
class RatorIdenExpectedException(CastException): pass
class RatorIdenUnexpectedException(CastException): pass
class RedefinitionException(CastException): pass
class ScopeResolutionOrderException(CastException): pass
class ScopeUpdateMismatchException(CastException): pass
class TypedefUnexpectedException(CastException): pass

#------------------------------------------------------------------------------------------------------------------------
# SpecFlag
#------------------------------------------------------------------------------------------------------------------------

def SpecFlagMeta(name, bases, namespace, **kwds):
    cls = type(name, bases, namespace).init()
    for i,x in enumerate((
        ('StorageClasAuto', 'auto'), 
        ('StorageClasExtern', 'extern'), 
        ('StorageClasRegister', 'register'), 
        ('StorageClasStatic', 'static'), 
        ('StorageClasThreadLocal', '_Thread_local'), 
        ('StorageClasTypedef', 'typedef'), 
        ('FunSpecInline', 'inline'), 
        ('FunSpecNoreturn', '_Noreturn'), 
        ('TypQualAtomic', '_Atomic'), 
        ('TypQualConst', 'const'), 
        ('TypQualRestrict', 'restrict'), 
        ('TypQualVolatile', 'volatile'), 
        ('TypQualSlstHex', '/*x*/'), 
        ('TypQualSlstId3v2Encoding', '/*id3v2Encoding*/'), 
        ('TypSpecSigned', 'signed'), 
        ('TypSpecUnsigned', 'unsigned'), 
        ('TypSpecComplex', '_Complex'), 
        ('TypSpecLong1', 'long'),
        ('TypSpecLong2', 'long long'),
        ('TypSpecShort', 'short'), 
        ('TypSpecBool', '_Bool'), 
        ('TypSpecChar', 'char'), 
        ('TypSpecDouble', 'double'), 
        ('TypSpecFloat', 'float'), 
        ('TypSpecInt', 'int'), 
        ('TypSpecVoid', 'void'), 
        ('TypSpecNprimitive', None),
    )):
        cls.add(x[0], 1<<i, 1<<i, cKeyword=x[1])
        
    cls.StorageClasMask = cls.maskFromIdenPre('StorageClas')
    cls.TypSpecMask =     cls.maskFromIdenPre('TypSpec')
    cls.TypQualMask =     cls.maskFromIdenPre('TypQual')
    cls.FunSpecMask =     cls.maskFromIdenPre('FunSpec')
    cls.Mask = cls.StorageClasMask | cls.TypSpecMask | cls.TypQualMask | cls.FunSpecMask
    cls.TopMask = (cls.StorageClasMask | cls.FunSpecMask) ^ cls.StorageClasTypedef 
    return cls

class SpecFlag(Denum, metaclass=SpecFlagMeta):
    @classmethod
    def canonFlags(cls, dst, flags):
        for item in cls.ItemV:
            if flags & item.val and None is not item.cKeyword:
                dst.append(item.cKeyword)
        return dst
    
#------------------------------------------------------------------------------------------------------------------------
# CanonClas
#------------------------------------------------------------------------------------------------------------------------

class CanonClas:
    Basic = 0
    Right = 1
    Ptr = 2

#------------------------------------------------------------------------------------------------------------------------
# PyTyp
#------------------------------------------------------------------------------------------------------------------------

def pyTypVFromStiV(stiV):
    # first pass calculates nominal PyTyp class to handle each sti
    for sti in stiV:
        sti.pyTypClas = sti.pyTypClasGet()

    # second pass calls class method pyTypVAdd on each sti.pyTypClas to add PyTyp-derived instances to pyTypV.
    # params stiV,i allow an invocation of pyTypVAdd to consume additional sti (e.g. ctyplib.BPyTyp).
    # usually the additionally consumed sti will have pyTypClas set to PyTypSkip
    pyTypV = []
    for i,sti in enumerate(stiV):
        sti.pyTypClas.pyTypVAdd(pyTypV, sti, stiV, i)
    return pyTypV

class PyTyp:
    @classmethod
    def b1P(cls): return False
    
    @classmethod
    def pyTypVAdd(cls, pyTypV, sti, stiV, i):
        pyTypV.append(cls(sti))

    def __init__(self, sti):
        self.sti = sti

    def getr(self, pre): return None 
    def setr(self, pre, valIden): return None 

class PyTypUnknown(PyTyp): pass

class PyTypSkip(PyTyp):
    @classmethod
    def pyTypVAdd(cls, pyTypV, sti, stiV, i): pass

#------------------------------------------------------------------------------------------------------------------------
# Typ
#------------------------------------------------------------------------------------------------------------------------

class Typ:
    def funP(self): return False
    def structP(self): return False
    def canonClas(self): return CanonClas.Basic
    
    def canon(self, up):
        childL,childR = self.canonLR()
        return f'{childL}{childR}' if None is up else f'{childL} {up}{childR}'

    def nick(self):
        return self.__class__.__name__[:-3]

    def uniq1(self, scope):
        return self

    def uniq1Norm(self, scope):
        return self

    def parseSpecFromThis(self, spec, scope):
        spec.child = self

    def parseSpecToTop(self, spec, scope):
        topFlags = SpecFlag.TopMask & spec.flags
        if None is not spec.alignas:
            return TypModAlignas(self, topFlags, spec.alignas).uniq1(scope)
        elif topFlags:
            return TypMod(self, topFlags).uniq1(scope)
        else:
            return self

    def pyTypClasGet(self): return PyTypUnknown
    def pyTypArrayClasGet(self): return PyTypUnknown
    def pyTypPtrClaxsGet(self): return PyTypUnknown

#------------------------------------------------------------------------------------------------------------------------
# TypArray
#------------------------------------------------------------------------------------------------------------------------

class TypArray(Typ):
    def canonClas(self): return CanonClas.Right

    def __init__(self, child, toks):
        super().__init__()
        self.child = child
        self.toks = toks

    def toksS(self):
        return ' '.join([tok.val for tok in self.toks])
        
    def dump(self, logr, pre):
        toks = None if self.toks is None else self.toksS()
        with logr(f'{pre}{self.__class__.__name__} [toks {toks}]'):
            if None is not self.child:
                self.child.dump(logr, '')
                
    def canonLR(self):
        childL,childR = self.child.canonLR()
        x = None if None is self.toks else self.toksS()
        return (childL, f'[{x}]{childR}')

    def uniq1(self, scope):
        return scope.glo.uniqtab.setdefault(('TypArray', id(self.child), *[tok.val for tok in self.toks]), self)

    def uniq1Norm(self, scope):
        return TypArray(self.child, []).uniq1(scope)

    def pyTypClasGet(self): return self.child.pyTypArrayClasGet()
    
#------------------------------------------------------------------------------------------------------------------------
# TypAtomic
#------------------------------------------------------------------------------------------------------------------------

class TypAtomic(Typ):
    def __init__(self, child):
        super().__init__()
        self.child = child
        
    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__}'):
            if None is not self.child:
                self.child.dump(logr, '')
            
    def canonLR(self):
        return (f'_Atomic({self.child.canon(None)})', '')
    
    def uniq1(self, scope):
        return scope.glo.uniqtab.setdefault(('TypAtomic', id(self.child)), self)

#------------------------------------------------------------------------------------------------------------------------
# TypEnum
#------------------------------------------------------------------------------------------------------------------------

class TypEnum(Typ):
    def __init__(self, iden):
        super().__init__()
        self.iden = iden
        self.items = None
        self.pos = None

    #todo-dep def idenStr(self):
    #    return '' if None is self.iden else self.iden
    
    def idenOrId(self):
        return f'<{id(self)}>' if None is self.iden else self.iden

    def itemsInit(self):
        if None is not self.items:
            raise RedefinitionException(pos)
        self.items = []

    def itemAdd(self, item):
        self.items.append(item)

    def dump(self, logr, pre):
        if None is self.items:
            logr(f'{pre}{self.__class__.__name__} {self.idenOrId()} <{self.pos}> [items None]')
        else:
            with logr(f'{pre}{self.__class__.__name__} {self.idenOrId()} <{self.pos}> [itemsN {len(self.items)}]'):
                for item in self.items:
                    item.dump(logr, '[item] ')

    def canonLR(self):
        dst = [ 'enum' ]
        if None is not self.iden:
            dst.append(self.iden)
        if None is not self.items:
            dst += ( '{', ', '.join([sti.canon() for sti in self.items]), '}')
        return (' '.join(dst), '')

#------------------------------------------------------------------------------------------------------------------------
# TypFun
#------------------------------------------------------------------------------------------------------------------------

class TypFun(Typ):
    def funP(self): return True
    def canonClas(self): return CanonClas.Right

    def __init__(self, child):
        super().__init__()
        self.child = child
        self.paramV = []

    def paramAdd(self, sti):
        self.paramV.append(sti)
        
    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__}'):
            if None is not self.paramV:
                for param in self.paramV:
                    param.dump(logr, '[param] ')
            if None is not self.child:
                self.child.dump(logr, '')
            
    def canonLR(self):
        childL,childR = self.child.canonLR()
        x = ', '.join([sti.canon() for sti in self.paramV])
        return (childL, f'({x}){childR}')
    
    def uniq1(self, scope):
        return scope.glo.uniqtab.setdefault(('TypFun', id(self.child), *[id(param) for param in self.paramV]), self)

#------------------------------------------------------------------------------------------------------------------------
# TypIden

class TypIden(Typ):
    def __init__(self, iden):
        super().__init__()
        self.iden = iden 
        
    def dump(self, logr, pre):
        logr(f'{pre}{self.__class__.__name__} {self.iden}')

    def canonLR(self):
        return (self.iden, '')

#------------------------------------------------------------------------------------------------------------------------
# TypMod
#------------------------------------------------------------------------------------------------------------------------

class TypMod(Typ):
    def __init__(self, child, flags):
        super().__init__()
        self.child = child
        self.flags = flags

    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__} [flags {SpecFlag.des(self.flags)}]'):
            if None is not self.child:
                self.child.dump(logr, '')

    def canonLR(self):
        childL,childR = self.child.canonLR()
        l = SpecFlag.canonFlags([], SpecFlag.TopMask & self.flags)
        if CanonClas.Ptr == self.child.canonClas():
            l.append(childL)
            SpecFlag.canonFlags(l, SpecFlag.TypQualMask & self.flags)
        else:
            SpecFlag.canonFlags(l, SpecFlag.TypQualMask & self.flags)
            l.append(childL)
        return (' '.join(l), childR)

    def uniq1(self, scope):
        return scope.glo.uniqtab.setdefault(('TypMod', id(self.child), self.flags), self)
        
    def parseSpecFromThis(self, spec, scope):
        spec.child = self.child
        spec.flags |= self.flags
        
    def parseSpecToTop(self, spec, scope):
        topFlags = SpecFlag.TopMask & spec.flags
        if None is not spec.alignas:
            return TypModAlignas(self.child, self.flags | topFlags, spec.alignas).uniq1(scope)
        elif topFlags:
            return TypMod(self.child, self.flags | topFlags).uniq1(scope)
        else:
            return self

    def pyTypClasGet(self): return self.child.pyTypClasGet()
    def pyTypArrayClasGet(self): return self.child.pyTypArrayClasGet()
    def pyTypPtrClasGet(self): return self.child.pyTypPtrClasGet()

#------------------------------------------------------------------------------------------------------------------------
# TypModAlignas
#------------------------------------------------------------------------------------------------------------------------

class TypModAlignas(TypMod):
    def __init__(self, child, flags, alignas):
        super().__init__(child, flags)
        self.alignas = alignas
        
    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__} [flags {SpecFlag.des(self.flags)}]'):
            self.alignas.dump(logr, '[alignas] ')
            if None is not self.child:
                self.child.dump(logr, '')

    def canonLR(self):
        childL,childR = self.child.canonLR()
        l = [f"_Alignas({' '.join([tok.val for tok in self.alignas])})"]
        SpecFlag.canonFlags(l, SpecFlag.TopMask & self.flags)
        if CanonClas.Ptr == self.child.canonClas():
            l.append(childL)
            SpecFlag.canonFlags(l, SpecFlag.TypQualMask & self.flags)
        else:
            SpecFlag.canonFlags(l, SpecFlag.TypQualMask & self.flags)
            l.append(childL)
        return (' '.join(l), childR)

    def uniq1(self, scope):
        return scope.glo.uniqtab.setdefault(('TypModAlignas', id(self.child), topFlags, id(self.alignas)), self)

    def parseSpecFromThis(self, spec, scope):
        spec.child = self.child
        spec.flags |= self.flags
        if None is spec.alignas:
            spec.alignas = self.alignas
                
    def parseSpecToTop(self, spec, scope):
        topFlags = SpecFlag.TopMask & spec.flags
        return TypModAlignas(self.child, self.flags | topFlags, self.alignas).uniq1(scope)

#------------------------------------------------------------------------------------------------------------------------
# TypPrim

class TypPrim(Typ):
    def __init__(self, flags):
        super().__init__()
        self.flags = flags
        
    def dump(self, logr, pre):
        logr(f'{pre}{self.__class__.__name__} {SpecFlag.des(self.flags)}')

    def canonLR(self):
        return (' '.join(SpecFlag.canonFlags([], self.flags)), '')

#------------------------------------------------------------------------------------------------------------------------
# TypPtr
#------------------------------------------------------------------------------------------------------------------------

class TypPtr(Typ):
    def canonClas(self): return CanonClas.Ptr
    
    def __init__(self, child):
        super().__init__()
        self.child = child
    
    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__}'):
            if None is not self.child:
                self.child.dump(logr, '')

    def canonLR(self):
        childL,childR = self.child.canonLR()
        if CanonClas.Right == self.child.canonClas():
            return (f'{childL} (*', f'){childR}')
        else:
            return (f'{childL} *', childR)

    def uniq1(self, scope):
        return scope.glo.uniqtab.setdefault(('TypPtr', id(self.child)), self)
    
    def pyTypClasGet(self): return self.child.pyTypPtrClasGet()

#------------------------------------------------------------------------------------------------------------------------
# TypSu TypStruct TypUnion
#------------------------------------------------------------------------------------------------------------------------

class TypSu(Typ):
    def __init__(self, iden):
        super().__init__()
        self.iden = iden
        self.items = None
        self.pos = None

    #todo-dep def idenStr(self):
    #    return '' if None is self.iden else self.iden
    
    def idenOrId(self):
        return f'<{id(self)}>' if None is self.iden else self.iden

    def itemsInit(self):
        if None is not self.items:
            raise RedefinitionException(pos)
        self.items = []

    def itemAdd(self, sti):
        self.items.append(sti)
        
    def dump(self, logr, pre):
        if None is self.items:
            logr(f'{pre}{self.__class__.__name__} {self.idenOrId()} <{self.pos}> [items None]')
        else:
            with logr(f'{pre}{self.__class__.__name__} {self.idenOrId()} <{self.pos}> [itemsN {len(self.items)}]'):
                for item in self.items:
                    item.dump(logr, '[item] ')
                    
    def canonLR(self):
        dst = [ self.KeywordC ]
        if None is not self.iden:
            dst.append(self.iden)
        if None is not self.items:
            dst += ( '{', '; '.join([sti.canon() for sti in self.items]), '}')
        return (' '.join(dst), '')

class TypStruct(TypSu):
    def structP(self): return True
    KeywordC = 'struct'
    
class TypUnion(TypSu):
    KeywordC = 'union'

#------------------------------------------------------------------------------------------------------------------------
# TypUnknown
#------------------------------------------------------------------------------------------------------------------------

class TypUnknown(Typ):
    def __init__(self, iden):
        super().__init__()
        self.iden = iden

    def dump(self, logr, pre):
        logr(f'{pre}{self.__class__.__name__} {self.iden}')

    def canonLR(self):
        return (f'<UNKNOWN {self.iden}>', '')
    
#------------------------------------------------------------------------------------------------------------------------
# ParseSpec
#------------------------------------------------------------------------------------------------------------------------

class ParseSpec:
    def __init__(self):
        self.child = None
        self.flags = 0
        self.alignas = None

    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__}'):
            logr(f'[child] {self.child!r}')
            logr(f'[flags] {self.flags!r}')
            logr(f'[alignas] {self.alignas!r}')
        
    def ratorRevStiUniq(self, scope, rev):
        child = self.child
        while None is not rev:
            x = rev
            rev = rev.child
            x.child = child
            child = x.uniq1(scope)
        # assert: child is an sti

        child.child = child.child.parseSpecToTop(self, scope)
        return child
        
#------------------------------------------------------------------------------------------------------------------------
# SymtabItem
#
# also used for paramList, struct/union
#------------------------------------------------------------------------------------------------------------------------

class SymtabItem:
    def typP(self): return False
    
    def __init__(self, iden, child, pos):
        self.iden = iden
        self.child = child
        self.pos = pos

    def copy(self):
        return SymtabItem(self.iden, self.child, None)
        
    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__} {self.iden} <{self.pos}>'):
            if None is not self.child:
                self.child.dump(logr, '')
                logr(f'[canon] {self.canon()}')
                
    def canon(self):
        return self.iden if None is self.child else self.child.canon(self.iden)

    def uniq1(self, scope):
        return self

    def toAtomic(self, spec):
        if None is not self.iden:
            raise RatorIdenUnexpectedException(self.pos)
        if SpecFlag.StorageClasTypedef & spec.flags:
            raise TypedefUnexpectedException(self.pos)
        return TypAtomic(self.child)

    def toDecl(self, spec):
        if None is self.iden:
            raise RatorIdenExpectedException(self.pos)
        if SpecFlag.StorageClasTypedef & spec.flags:
            return SymtabItemTypedef(self.iden, self.child, self.pos)
        return self

    def toDeclBitfield(self, spec, bitfield):
        if None is self.iden:
            raise RatorIdenExpectedException(self.pos)
        if SpecFlag.StorageClasTypedef & spec.flags:
            raise TypedefUnexpectedException(self.pos)
        return SymtabItemBitfield(self.iden, self.child, self.pos, bitfield)

    def toDeclInitr(self, spec, initr):
        if None is self.iden:
            raise RatorIdenExpectedException(self.pos)
        if SpecFlag.StorageClasTypedef & spec.flags:
            raise TypedefUnexpectedException(self.pos)
        return SymtabItemInitr(self.iden, self.child, self.pos, initr)

    def toParam(self, spec):
        if SpecFlag.StorageClasTypedef & spec.flags:
            raise TypedefUnexpectedException(self.pos)
        return self
    
class SymtabItemBitfield(SymtabItem):
    def __init__(self, iden, child, pos, bitfield):
        super().__init__(iden, child, pos)
        self.bitfield = bitfield
        
    def dump(self, logr, pre):
        bitfield = ' '.join([tok.val for tok in self.bitfield])
        with logr(f'{pre}{self.__class__.__name__} {self.iden} <{self.pos}> [bitfield {bitfield}]'):
            if None is not self.child:
                self.child.dump(logr, '')
                logr(f'[canon] {self.canon()}')
    
    def canon(self):
        x = ' '.join([tok.val for tok in self.bitfield])
        return f'{super().canon()} : {x}'

class SymtabItemInitr(SymtabItem):
    def __init__(self, iden, child, pos, initr):
        super().__init__(iden, child, pos)
        self.initr = initr
        
    def dump(self, logr, pre):
        initr = ' '.join([tok.val for tok in self.initr])
        with logr(f'{pre}{self.__class__.__name__} {self.iden} <{self.pos}> [initr {initr}]'):
            if None is not self.child:
                self.child.dump(logr, '')
                logr(f'[canon] {self.canon()}')

    def canon(self):
        x = ' '.join([tok.val for tok in self.initr])
        return f'{super().canon()} = {x}'

class SymtabItemTypedef(SymtabItem):
    def typP(self): return True
    
    def canon(self):
        return f'typedef {super().canon()}'
    
#------------------------------------------------------------------------------------------------------------------------
# SymtabItemIterator
#------------------------------------------------------------------------------------------------------------------------

class SymtabItemIterator:
    def __init__(self, v, pre=None):
        self.v = v[:]
        self.i = 0
        #self.cur 
        
    def __iter__(self):
        return self
        
    def __next__(self):
        while self.i < len(self.v):
            self.cur = self.v[self.i]
            self.i += 1
            if None is not self.cur:
                return self.cur
        raise StopIteration()

    def nextIs(self, isMeth):
        if self.i < len(self.v):
            if None is not (cur1 := self.v[self.i]):
                if getattr(cur1, isMeth)():
                    self.i += 1
                    return cur1
        return None
        
#------------------------------------------------------------------------------------------------------------------------
# ScopeGlo
#------------------------------------------------------------------------------------------------------------------------
        
class ScopeGlo:
    def __init__(self):
        self.uniqtab = {}

#------------------------------------------------------------------------------------------------------------------------
# Scope
#------------------------------------------------------------------------------------------------------------------------

class Scope:
    def __init__(self, glo, *upV):
        self.glo = glo
        self.upV = upV
        self.idenStiD = {}
        self.primTypD = {}
        self.enumTypD = {}
        self.structTypD = {}
        self.unionTypD = {}

    def dn(self):
        return Scope(self.glo, self)

    def updateDict(self, d, od):
        for ok,ov in od.items():
            if None is (v := d.get(ok)):
                d[ok] = ov
            elif v is not ov:
                raise ScopeUpdateMismatchException(ok, v, ov)

    def update(self, other):
        self.updateDict(self.idenStiD, other.idenStiD)
        self.updateDict(self.primTypD, other.primTypD)
        self.updateDict(self.enumTypD, other.enumTypD)
        self.updateDict(self.structTypD, other.structTypD)
        self.updateDict(self.unionTypD, other.unionTypD)
    
    #--------------------------------------------------------------------------------------------------------------------
    # typ-specific

    def idenGet(self, iden):
        if None is not (sti := self.idenStiD.get(iden)):
            return sti
        for up in self.upV:
            if None is not (sti := up.idenGet(iden)):
                return sti
        return None

    def idenGetVPre(self, pre):
        stiV = []
        for sti in self.idenStiD.values():
            if sti.iden.startswith(pre):
                sti.idenS = sti.iden[len(pre):]
                stiV.append(sti)
        return stiV

    def idenPutSti(self, sti):
        self.idenStiD[sti.iden] = sti
        return self

    def idenPutTyp(self, typ, pos):
        sti = SymtabItemTypedef(typ.iden, typ, pos)
        self.idenStiD[sti.iden] = sti
        return sti

    def primGet(self, flags):
        if None is not (typ := self.primTypD.get(flags)):
            return typ
        for up in self.upV:
            if None is not (typ := up.primGet(flags)):
                return typ
        return None
    
    def primPut(self, typ, *aliasFlagss):
        self.primTypD[typ.flags] = typ
        for flags in aliasFlagss:
            self.primTypD[flags] = typ
        return typ

    def enumGet(self, iden):
        if None is not (typ := self.enumTypD.get(iden)):
            return typ
        for up in self.upV:
            if None is not (typ := up.enumGet(iden)):
                return typ
        return None

    def enumGetOrNew(self, iden):
        if None is (typ := self.enumGet(iden)):
            typ = self.enumTypD[iden] = TypEnum(iden)
        return typ
    
    def enumNewAnon(self):
        typ = TypEnum(None)
        self.enumTypD[id(typ)] = typ
        return typ

    def structGet(self, iden):
        if None is not (typ := self.structTypD.get(iden)):
            return typ
        for up in self.upV:
            if None is not (typ := up.structGet(iden)):
                return typ
        return None

    def structGetOrNew(self, iden):
        if None is (typ := self.structGet(iden)):
            typ = self.structTypD[iden] = TypStruct(iden)
        return typ
    
    def structNewAnon(self):
        typ = TypStruct(None)
        self.structTypD[id(typ)] = typ
        return typ

    def unionGet(self, iden):
        if None is not (typ := self.unionTypD.get(iden)):
            return typ
        for up in self.upV:
            if None is not (typ := up.unionGet(iden)):
                return typ
        return None

    def unionGetOrNew(self, iden):
        if None is (typ := self.unionGet(iden)):
            typ = self.unionTypD[iden] = TypUnion(iden)
        return typ
    
    def unionNewAnon(self):
        typ = TypUnion(None)
        self.unionTypD[id(typ)] = typ
        return typ

    #--------------------------------------------------------------------------------------------------------------------
    # dump
    
    def dump(self, logr, pre, dumpUp=0):
        with logr(f'{pre}{self.__class__.__name__}'):
            if dumpUp:
                for up in self.upV:
                    with logr('[up]'):
                        up.dump(logr, pre, dumpUp)
            for flags,typ in self.primTypD.items():
                typ.dump(logr, f'prim {SpecFlag.des(flags)}: ')
            for iden,typ in self.enumTypD.items():
                typ.dump(logr, f'enum {iden!r}: ')
            for iden,typ in self.structTypD.items():
                typ.dump(logr, f'struct {iden!r}: ')
            for iden,typ in self.unionTypD.items():
                typ.dump(logr, f'union {iden!r}: ')
            for iden,sti in self.idenStiD.items():
                sti.dump(logr, f'{iden!r}: ')
                
    def dumpCanon(self, logr, pre, dumpUp=0):
        with logr(f'{pre}{self.__class__.__name__}'):
            if dumpUp:
                for up in self.upV:
                    with logr('[up]'):
                        up.dumpCanon(logr, pre, dumpUp)
            for flags,typ in self.primTypD.items():
                logr(f'prim {SpecFlag.des(flags)}: {typ.canon(None)}')
            for iden,typ in self.enumTypD.items():
                logr(f'enum {iden!r}: {typ.canon(None)}')
            for iden,typ in self.structTypD.items():
                logr(f'struct {iden!r}: {typ.canon(None)}')
            for iden,typ in self.unionTypD.items():
                logr(f'union {iden!r}: {typ.canon(None)}')
            for iden,sti in self.idenStiD.items():
                logr(f'{iden!r}: {sti.canon()}')

