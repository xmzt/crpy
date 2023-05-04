from .castlib import PyTyp,PyTypSkip,Scope,ScopeGlo,SpecFlag,TypIden,TypPrim

#------------------------------------------------------------------------------------------------------------------------
# PyTyp
#------------------------------------------------------------------------------------------------------------------------

class BPyTyp(PyTyp):
    def __init__(self, sti, sti1):
        self.sti = sti
        self.sti1 = sti1

    def getr(self, pre):
        return f'crpyPyBytesFromStringAB({pre}{self.sti.iden}, {pre}{self.sti1.iden})'
    
class ComplexFloatPyTyp(PyTyp): pass
    
class FloatPyTyp(PyTyp):
    def getr(self, pre): return f'PyFloat_FromDouble({pre}{self.sti.iden})'

class Id3v2EncodingPyTyp(PyTyp):
    def getr(self, pre): return f'PyLong_FromUnsignedLong({pre}{self.sti.iden})'
    def fmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}!r}}'

class Id32PyTyp(PyTyp):
    def getr(self, pre): return f'PyBytes_FromStringAndSize((const char*){pre}{self.sti.iden}.u8s, 4)'
    def fmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}!r}}'

class Id128PyTyp(PyTyp):
    def getr(self, pre): return f'PyBytes_FromStringAndSize((const char*){pre}{self.sti.iden}.u8s, 16)'
    def fmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}.hex()}}'
    
class LongPyTyp(PyTyp):
    def getr(self, pre): return f'PyLong_FromLong({pre}{self.sti.iden})'

class PyObjectPtrPyTyp(PyTyp):
    def getr(self, pre): return f'{pre}{self.sti.iden}'
    def fmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}!r}}'

class U8PtrPyTyp(PyTyp):
    @classmethod
    def b1P(cls): return True

    @classmethod
    def pyTypVAdd(cls, pyTypV, sti, stiV, i):
        if (j := i+1) < len(stiV) and (sti1 := stiV[j]).pyTypClas.b1P():
            sti1.pyTypClas = PyTypSkip
            pyTypV.append(BPyTyp(sti, sti1))
        else:
            pyTypV.append(cls(sti))

class UlongPyTyp(PyTyp):
    def getr(self, pre): return f'PyLong_FromUnsignedLong({pre}{self.sti.iden})'

class VoidPtrPyTyp(PyTyp):
    def getr(self, pre): return f'PyBytes_FromStringAndSize((const char*){pre}{self.sti.iden}, sizeof(void*))'
    def fmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}.hex()}}'

class XUPyTyp(PyTyp):
    def fmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:x}}'

class XU8PyTyp(PyTyp):
    def fmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:02x}}'

class XU16PyTyp(PyTyp):
    def fmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:04x}}'

class XU32PyTyp(PyTyp):
    def fmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:08x}}'

class XU64PyTyp(PyTyp):
    def fmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:016x}}'

class ZArrayPyTyp(PyTyp):
    def getr(self, pre): return f'McpyTupleSize_t({pre}{self.sti.iden}, {self.sti.child.toksS()})'
    def fmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}}}'

#------------------------------------------------------------------------------------------------------------------------
# TypPrim
#------------------------------------------------------------------------------------------------------------------------

class BoolTyp(TypPrim):
    def pyTypClasGet(self): return LongPyTyp

class CTyp(TypPrim):
    def pyTypClasGet(self): return LongPyTyp

class CDTyp(TypPrim):
    def pyTypClasGet(self): return ComplexFloatPyTyp
    
class CFTyp(TypPrim):
    def pyTypClasGet(self): return ComplexFloatPyTyp
    
class CLDTyp(TypPrim):
    def pyTypClasGet(self): return ComplexFloatPyTyp
    
class DTyp(TypPrim):
    def pyTypClasGet(self): return FloatPyTyp

class FTyp(TypPrim):
    def pyTypClasGet(self): return FloatPyTyp
    
class ITyp(TypPrim):
    def pyTypClasGet(self): return LongPyTyp
    
class LTyp(TypPrim):
    def pyTypClasGet(self): return LongPyTyp
    
class LDTyp(TypPrim):
    def pyTypClasGet(self): return FloatPyTyp

class LLTyp(TypPrim):
    def pyTypClasGet(self): return LongPyTyp
    
class STyp(TypPrim):
    def pyTypClasGet(self): return LongPyTyp
    
class UTyp(TypPrim):
    def pyTypClasGet(self): return UlongPyTyp
    
class UCTyp(TypPrim):
    def pyTypClasGet(self): return UlongPyTyp
    
class ULTyp(TypPrim):
    def pyTypClasGet(self): return UlongPyTyp
    
class ULLTyp(TypPrim):
    def pyTypClasGet(self): return UlongPyTyp
    
class USTyp(TypPrim):
    def pyTypClasGet(self): return UlongPyTyp
    
class VoidTyp(TypPrim): pass

#------------------------------------------------------------------------------------------------------------------------
# TypIden
#------------------------------------------------------------------------------------------------------------------------

class I8Typ(TypIden):
    def pyTypClasGet(self): return LongPyTyp
    
class I16Typ(TypIden):
    def pyTypClasGet(self): return LongPyTyp
    
class I32Typ(TypIden):
    def pyTypClasGet(self): return LongPyTyp
    
class I64Typ(TypIden):
    def pyTypClasGet(self): return LongPyTyp
    
class U8Typ(TypIden):
    def pyTypClasGet(self): return UlongPyTyp
    def pyTypPtrClasGet(self): return U8PtrPyTyp
    
class U16Typ(TypIden):
    def pyTypClasGet(self): return UlongPyTyp
    
class U32Typ(TypIden):
    def pyTypClasGet(self): return UlongPyTyp
    
class U64Typ(TypIden):
    def pyTypClasGet(self): return UlongPyTyp
    
class ZTyp(TypIden):
    def pyTypClasGet(self): return UlongPyTyp
    def pyTypArrayClasGet(self): return ZArrayPyTyp
    
class Id32Typ(TypIden):
    def pyTypClasGet(self): return Id32PyTyp

class Id128Typ(TypIden):
    def pyTypClasGet(self): return Id128PyTyp
    
class PyObjectTyp(TypIden):
    def pyTypPtrClasGet(self): return PyObjectPtrPyTyp

#------------------------------------------------------------------------------------------------------------------------
# init
#------------------------------------------------------------------------------------------------------------------------

def initScope0(fragr):
    scope = Scope(ScopeGlo())
    scope.primPut(BoolTyp(SpecFlag.TypSpecBool))
    scope.primPut(CTyp(SpecFlag.TypSpecChar), # todo signed or unsigned
                  SpecFlag.TypSpecSigned | SpecFlag.TypSpecChar)
    scope.primPut(CDTyp(SpecFlag.TypSpecComplex | SpecFlag.TypSpecDouble))
    scope.primPut(CFTyp(SpecFlag.TypSpecComplex | SpecFlag.TypSpecFloat))
    scope.primPut(CLDTyp(SpecFlag.TypSpecComplex | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecDouble))
    scope.primPut(DTyp(SpecFlag.TypSpecDouble))
    scope.primPut(FTyp(SpecFlag.TypSpecFloat))
    scope.primPut(ITyp(SpecFlag.TypSpecInt),
                  SpecFlag.TypSpecSigned,
                  SpecFlag.TypSpecSigned | SpecFlag.TypSpecInt)
    scope.primPut(LTyp(SpecFlag.TypSpecLong1),
                  SpecFlag.TypSpecLong1 | SpecFlag.TypSpecInt,
                  SpecFlag.TypSpecSigned | SpecFlag.TypSpecLong1,
                  SpecFlag.TypSpecSigned | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecInt)
    scope.primPut(LDTyp(SpecFlag.TypSpecLong1 | SpecFlag.TypSpecDouble))
    scope.primPut(LLTyp(SpecFlag.TypSpecLong2),
                  SpecFlag.TypSpecLong2 | SpecFlag.TypSpecInt,
                  SpecFlag.TypSpecSigned | SpecFlag.TypSpecLong2,
                  SpecFlag.TypSpecSigned | SpecFlag.TypSpecLong2 | SpecFlag.TypSpecInt)
    scope.primPut(STyp(SpecFlag.TypSpecShort),
                  SpecFlag.TypSpecShort | SpecFlag.TypSpecInt,
                  SpecFlag.TypSpecSigned | SpecFlag.TypSpecShort,
                  SpecFlag.TypSpecSigned | SpecFlag.TypSpecShort | SpecFlag.TypSpecInt)
    scope.primPut(UTyp(SpecFlag.TypSpecUnsigned),
                  SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecInt)
    scope.primPut(UCTyp(SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecChar))
    scope.primPut(ULTyp(SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecLong1),
                  SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecInt)
    scope.primPut(ULLTyp(SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecLong2),
                  SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecLong2 | SpecFlag.TypSpecInt)
    scope.primPut(USTyp(SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecShort),
                  SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecShort | SpecFlag.TypSpecInt)
    scope.primPut(VoidTyp(SpecFlag.TypSpecVoid))

    scope.idenPutTyp(I8Typ('int8_t'), None)
    scope.idenPutTyp(I16Typ('int16_t'), None)
    scope.idenPutTyp(I32Typ('int32_t'), None)
    scope.idenPutTyp(I64Typ('int64_t'), None)
    scope.idenPutTyp(U8Typ('uint8_t'), None)
    scope.idenPutTyp(U16Typ('uint16_t'), None)
    scope.idenPutTyp(U32Typ('uint32_t'), None)
    scope.idenPutTyp(U64Typ('uint64_t'), None)
    scope.idenPutTyp(ZTyp('size_t'), None)
    scope.idenPutTyp(Id32Typ('BitId32'), None)
    scope.idenPutTyp(Id128Typ('BitId128'), None)
    scope.idenPutTyp(PyObjectTyp('PyObject'), None)

    return scope

