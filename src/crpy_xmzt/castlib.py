from pylib0_xmzt.denumlib import Denum

class CastException(Exception): pass
class FlagsUnexpectedException(CastException): pass
class RatorIdenExpectedException(CastException): pass
class RatorIdenUnexpectedException(CastException): pass
class RedefinitionException(CastException): pass
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
        ('TypSpecLong2', 'long'),
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
# Typ
#------------------------------------------------------------------------------------------------------------------------

class Typ:
    def funP(self): return False
    def structP(self): return False
    def canonClas(self): return CanonClas.Basic
    
    def canon(self, up):
        childL,childR = self.canonLR()
        return f'{childL}{childR}' if None is up else f'{childL} {up}{childR}'

    def uniq1(self, symtab):
        return self

    def uniq1Norm(self, symtab):
        return self

    def parseSpecFromThis(self, spec, symtab):
        spec.child = self

    def parseSpecToTop(self, spec, symtab):
        topFlags = SpecFlag.TopMask & spec.flags
        if None is not spec.alignas:
            return TypModAlignas(self, topFlags, spec.alignas).uniq1(symtab)
        elif topFlags:
            return TypMod(self, topFlags).uniq1(symtab)
        else:
            return self

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

    def uniq1(self, symtab):
        return symtab.uniqtab.setdefault(('TypArray', id(self.child), *[tok.val for tok in self.toks]), self)

    def uniq1Norm(self, symtab):
        return TypArray(self.child, []).uniq1(symtab)
    
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
    
    def uniq1(self, symtab):
        return symtab.uniqtab.setdefault(('TypAtomic', id(self.child)), self)

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
    
    def uniq1(self, symtab):
        return symtab.uniqtab.setdefault(('TypFun', id(self.child), *[id(param) for param in self.paramV]), self)

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

    def uniq1(self, symtab):
        return symtab.uniqtab.setdefault(('TypMod', id(self.child), self.flags), self)
        
    def parseSpecFromThis(self, spec, symtab):
        spec.child = self.child
        spec.flags |= self.flags
        
    def parseSpecToTop(self, spec, symtab):
        topFlags = SpecFlag.TopMask & spec.flags
        if None is not spec.alignas:
            return TypModAlignas(self.child, self.flags | topFlags, spec.alignas).uniq1(symtab)
        elif topFlags:
            return TypMod(self.child, self.flags | topFlags).uniq1(symtab)
        else:
            return self

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

    def uniq1(self, symtab):
        return symtab.uniqtab.setdefault(('TypModAlignas', id(self.child), topFlags, id(self.alignas)), self)

    def parseSpecFromThis(self, spec, symtab):
        spec.child = self.child
        spec.flags |= self.flags
        if None is spec.alignas:
            spec.alignas = self.alignas
                
    def parseSpecToTop(self, spec, symtab):
        topFlags = SpecFlag.TopMask & spec.flags
        return TypModAlignas(self.child, self.flags | topFlags, self.alignas).uniq1(symtab)

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

    def uniq1(self, symtab):
        return symtab.uniqtab.setdefault(('TypPtr', id(self.child)), self)
    
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
        
    def ratorRevStiUniq(self, symtab, rev):
        child = self.child
        while None is not rev:
            x = rev
            rev = rev.child
            x.child = child
            child = x.uniq1(symtab)
        # assert: child is an sti

        child.child = child.child.parseSpecToTop(self, symtab)
        return child
        
#------------------------------------------------------------------------------------------------------------------------
# Mtyp
#------------------------------------------------------------------------------------------------------------------------
    
class Mtyp:
    #Nick = None

    def __init__(self, stiV):
        self.stiV = stiV
        
    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__} nick={self.Nick} stiV.n={len(self.stiV)}'):
            with logr(f'stiV'):
                for i,sti in enumerate(self.stiV):
                    sti.dump(logr, f'[{i}] ')
                
    def pyObjCode(self, fieldF): raise Exception()
    def pyFmt(self, fieldF): raise Exception()

class UnknownMtyp(Mtyp):
    Nick = 'unknown'
    
    def pyObjCode(self, fieldF): return f'PyUnicode_FromString("<UNIMPLEMENTED:{self.stiV[0].iden}>")'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}}}'

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

    def uniq1(self, symtab):
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
# Symtab Scope
#------------------------------------------------------------------------------------------------------------------------
        
class Symtab:
    def __init__(self):
        self.scope0 = { None:None }
        self.scope = self.scope0
        self.uniqtab = {}
        #todo del self.glo = {}
        self.mtypTrie = { None:None }
        
    def get(self, k):
        scope = self.scope
        while None is not scope:
            if None is not (x := scope.get(k)):
                return x
            scope = scope[None]
        return None

    def getVPre(self, pre):
        dst = []
        for k,sti in self.scope.items():
            if str is type(k) and sti.iden.startswith(pre):
                sti.idenS = sti.iden[len(pre):]
                dst.append(sti)
        return dst

    def scopeSetNew(self, scopeUp):
        self.scope = { None:scopeUp }
        return self.scope
        
    def scopeSetNew0(self):
        self.scope = { None:self.scope0 }
        return self.scope
    
    def scopePop(self):
        x = self.scope
        self.scope = self.scope[None]
        return x

    def scopePush(self):
        self.scope = { None:self.scope }
        return self.scope

    #--------------------------------------------------------------------------------------------------------------------
    # typ-specific

    def primGet(self, flags):
        return self.get(('p', flags))
    
    def primPut(self, typ, *aliasFlagss):
        sti = SymtabItemTypedef(('p', typ.flags), typ, None)
        self.scope[sti.iden] = sti
        for flags in aliasFlagss:
            self.scope[('p', flags)] = sti
        return sti

    def idenPut(self, typ, pos):
        sti = SymtabItemTypedef(typ.iden, typ, pos)
        self.scope[sti.iden] = sti
        return sti

    def enumNewAnon(self):
        x = TypEnum(None)
        sti = SymtabItemTypedef(('e', x.idenOrId()), x, None)
        self.scope[sti.iden] = sti
        return sti

    def enumGetOrNew(self, iden):
        if None is (sti := self.get(k := ('e', iden))):
            self.scope[k] = sti = SymtabItemTypedef(k, TypEnum(None), None)
        return sti
    
    def structNewAnon(self):
        x = TypStruct(None)
        sti = SymtabItemTypedef(('s', x.idenOrId()), x, None)
        self.scope[sti.iden] = sti
        return sti

    def structGetOrNew(self, iden):
        if None is (sti := self.get(k := ('s', iden))):
            self.scope[k] = sti = SymtabItemTypedef(k, TypStruct(None), None)
        return sti
    
    def unionNewAnon(self):
        x = TypUnion(None)
        sti = SymtabItemTypedef(('u', x.idenOrId()), x, None)
        self.scope[sti.iden] = sti
        return sti

    def unionGetOrNew(self, iden):
        if None is (sti := self.get(k := ('u', iden))):
            self.scope[k] = sti = SymtabItemTypedef(k, TypUnion(None), None)
        return sti

    def itemPut(self, item):
        self.scope[item.iden] = item
        return self

    #--------------------------------------------------------------------------------------------------------------------
    # dump

    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__}'):
            scope = self.scope
            while None is not scope:
                with logr(f'scope <{id(scope)}>'):
                    self.dumpScope(logr, scope)
                    scope = scope[None]
                
    def dumpScope(self, logr, scope):
        for k,v in scope.items():
            if None is not k:
                v.dump(logr, f'{k!r}: ')

    def dumpScopeCanon(self, logr, scope):
        for k,v in scope.items():
            if None is not k:
                logr(f'{k!r}: {v.canon()}')

    #--------------------------------------------------------------------------------------------------------------------
    # mtyp

    def mtypTriePutTypV(self, typV, mtypClas):
        b0 = self.mtypTrie
        for typ in typV:
            typId = id(typ)
            if None is (b1 := b0.get(typId)):
                b1 = b0[typId] = { None:None }
            b0 = b1
        b0[None] = mtypClas

    def mtypTrieMtypVFromStiV(self, mtypV, stiV, keyFromSti):
        iE = len(stiV)
        i = 0
        b0 = self.mtypTrie
        runClas = UnknownMtyp
        runA = i
        runE = i + 1
        while True:
            if i < iE and None is not (b1 := b0.get(keyFromSti(stiV[i]))):
                b0 = b1
                i += 1
                if None is not (clas := b0[None]):
                    runClas = clas
                    runE = i
            elif runA < iE:
                mtypV.append(runClas(stiV[runA:runE]))
                i = runE
                b0 = self.mtypTrie
                runClas = UnknownMtyp
                runA = i
                runE = i + 1
            else:
                break
        return mtypV
