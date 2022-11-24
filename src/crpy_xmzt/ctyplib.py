from .castlib import Mtyp,SpecFlag,Symtab,TypIden,TypPrim
from .cfraglib import Fragr

#------------------------------------------------------------------------------------------------------------------------
# Mtyp abstract
#------------------------------------------------------------------------------------------------------------------------

class ComplexFloatMtyp(Mtyp): pass
    
class FloatMtyp(Mtyp):
    def pyObjCode(self, fieldF): return f'PyFloat_FromDouble({fieldF(self.stiV[0])})'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}}}'

class LongMtyp(Mtyp):
    def pyObjCode(self, fieldF): return f'PyLong_FromLong({fieldF(self.stiV[0])})'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}}}'

class UlongMtyp(Mtyp):
    def pyObjCode(self, fieldF): return f'PyLong_FromUnsignedLong({fieldF(self.stiV[0])})'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}}}'
    
#------------------------------------------------------------------------------------------------------------------------
# Mtyp concrete
#------------------------------------------------------------------------------------------------------------------------

class BoolMtyp(LongMtyp): Nick = 'bool'
class CMtyp(LongMtyp): Nick = 'c'
class CDMtyp(ComplexFloatMtyp): Nick = 'cd'
class CFMtyp(ComplexFloatMtyp): Nick = 'cf'
class CLDMtyp(ComplexFloatMtyp): Nick = 'cld'
class DMtyp(FloatMtyp): Nick = 'd'
class FMtyp(FloatMtyp): Nick = 'f'
class IMtyp(LongMtyp): Nick = 'i'
class I8Mtyp(LongMtyp): Nick = 'i8'
class I16Mtyp(LongMtyp): Nick = 'i16'
class I32Mtyp(LongMtyp): Nick = 'i32'
class I64Mtyp(LongMtyp): Nick = 'i64'
class LMtyp(LongMtyp): Nick = 'l'
class LDMtyp(FloatMtyp): Nick = 'ld'
class LLMtyp(LongMtyp): Nick = 'll'
class SMtyp(LongMtyp): Nick = 's'
class UMtyp(UlongMtyp): Nick = 'u'
class U8Mtyp(UlongMtyp): Nick = 'u8'
class U16Mtyp(UlongMtyp): Nick = 'u16'
class U32Mtyp(UlongMtyp): Nick = 'u32'
class U64Mtyp(UlongMtyp): Nick = 'u64'
class UCMtyp(UlongMtyp): Nick = 'uc'
class ULMtyp(UlongMtyp): Nick = 'ul'
class ULLMtyp(UlongMtyp): Nick = 'ull'
class USMtyp(UlongMtyp): Nick = 'us'
class VoidMtyp(Mtyp): Nick = 'void'
class ZMtyp(UlongMtyp): Nick = 'z'

class BMtyp(Mtyp):
    Nick = 'b'
    def pyObjCode(self, fieldF):
        a = fieldF(self.stiV[0])
        b = fieldF(self.stiV[1])
        return f'PyBytes_FromStringAndSize((const char*){a}, {b} - {a})'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}!r}}'

class Id32Mtyp(Mtyp):
    Nick = 'id32'
    def pyObjCode(self, fieldF): return f'PyBytes_FromStringAndSize((const char*){fieldF(self.stiV[0])}.u8s, 4)'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}!r}}'

class Id128Mtyp(Mtyp):
    Nick = 'id128'
    def pyObjCode(self, fieldF): return f'PyBytes_FromStringAndSize((const char*){fieldF(self.stiV[0])}.u8s, 16)'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}.hex()}}'
    
class Id3v2EncodingMtyp(Mtyp):
    Nick = 'id3v2Encoding'
    def pyObjCode(self, fieldF): return f'PyLong_FromUnsignedLong({fieldF(self.stiV[0])})'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}!r}}'

class PyObjectMtyp(Mtyp):
    Nick = 'pyo'
    pass

class PyObjectPtrMtyp(Mtyp):
    Nick = 'pyoPtr'
    def pyObjCode(self, fieldF): return fieldF(self.stiV[0])
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}!r}}'

class ZArrayMtyp(Mtyp):
    Nick = 'zarray'
    def pyObjCode(self, fieldF): return f'McpyTupleSize_t({fieldF(self.stiV[0])}, {self.stiV[0].child.toksS()})'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}}}'

class VoidPtrMtyp(Mtyp):
    Nick = 'voidPtr'
    def pyObjCode(self, fieldF): return f'PyBytes_FromStringAndSize((const char*){fieldF(self.stiV[0])}, sizeof(void*))'
    def pyFmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}.hex()}}'

class XUMtyp(UlongMtyp):
    Nick = 'xu'
    def pyFmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:x}}'

class XU8Mtyp(UlongMtyp):
    Nick = 'xu8'
    def pyFmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:02x}}'

class XU16Mtyp(UlongMtyp):
    Nick = 'xu16'
    def pyFmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:04x}}'

class XU32Mtyp(UlongMtyp):
    Nick = 'xu32'
    def pyFmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:08x}}'

class XU64Mtyp(UlongMtyp):
    Nick = 'xu64'
    def pyFmt(self, fieldF): return f'0x{{{fieldF(self.stiV[0])}:016x}}'

#------------------------------------------------------------------------------------------------------------------------
# init
#------------------------------------------------------------------------------------------------------------------------

def fragrPopulate0(fragr):
    fragr.specSlst = 1

    def addPrim(mtypClas, typFlags, *flagss):
        typ = TypPrim(typFlags)
        fragr.symtab.primPut(typ, *flagss)
        fragr.symtab.mtypTriePutTypV((typ,), mtypClas)

    addPrim(BoolMtyp, SpecFlag.TypSpecBool)
    addPrim(CMtyp, SpecFlag.TypSpecChar, # todo signed or unsigned
            SpecFlag.TypSpecSigned | SpecFlag.TypSpecChar)
    addPrim(CDMtyp, SpecFlag.TypSpecComplex | SpecFlag.TypSpecDouble)
    addPrim(CFMtyp, SpecFlag.TypSpecComplex | SpecFlag.TypSpecFloat)
    addPrim(CLDMtyp, SpecFlag.TypSpecComplex | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecDouble)
    addPrim(DMtyp, SpecFlag.TypSpecDouble)
    addPrim(FMtyp, SpecFlag.TypSpecFloat)
    addPrim(IMtyp, SpecFlag.TypSpecInt,
            SpecFlag.TypSpecSigned,
            SpecFlag.TypSpecSigned | SpecFlag.TypSpecInt)
    addPrim(LMtyp, SpecFlag.TypSpecLong1,
            SpecFlag.TypSpecLong1 | SpecFlag.TypSpecInt,
            SpecFlag.TypSpecSigned | SpecFlag.TypSpecLong1,
            SpecFlag.TypSpecSigned | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecInt)
    addPrim(LDMtyp, SpecFlag.TypSpecLong1 | SpecFlag.TypSpecDouble)
    addPrim(LLMtyp, SpecFlag.TypSpecLong1 | SpecFlag.TypSpecLong2,
            SpecFlag.TypSpecLong1 | SpecFlag.TypSpecLong2 | SpecFlag.TypSpecInt,
            SpecFlag.TypSpecSigned | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecLong2,
            SpecFlag.TypSpecSigned | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecLong2 | SpecFlag.TypSpecInt)
    addPrim(SMtyp, SpecFlag.TypSpecShort,
            SpecFlag.TypSpecShort | SpecFlag.TypSpecInt,
            SpecFlag.TypSpecSigned | SpecFlag.TypSpecShort,
            SpecFlag.TypSpecSigned | SpecFlag.TypSpecShort | SpecFlag.TypSpecInt)
    addPrim(UMtyp, SpecFlag.TypSpecUnsigned,
            SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecInt)
    addPrim(UCMtyp, SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecChar)
    addPrim(ULMtyp, SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecLong1,
            SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecInt)
    addPrim(ULLMtyp, SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecLong2,
            SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecLong1 | SpecFlag.TypSpecLong2 | SpecFlag.TypSpecInt)
    addPrim(USMtyp, SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecShort,
            SpecFlag.TypSpecUnsigned | SpecFlag.TypSpecShort | SpecFlag.TypSpecInt)
    addPrim(VoidMtyp, SpecFlag.TypSpecVoid)

    def addIden(mtypClas, typIden):
        typ = TypIden(typIden)
        fragr.symtab.idenPut(typ, None)
        fragr.symtab.mtypTriePutTypV((typ,), mtypClas)

    addIden(I8Mtyp, 'int8_t')
    addIden(I16Mtyp, 'int16_t')
    addIden(I32Mtyp, 'int32_t')
    addIden(I64Mtyp, 'int64_t')
    addIden(U8Mtyp, 'uint8_t')
    addIden(U16Mtyp, 'uint16_t')
    addIden(U32Mtyp, 'uint32_t')
    addIden(U64Mtyp, 'uint64_t')
    addIden(ZMtyp, 'size_t')
    addIden(Id32Mtyp, 'BitId32')
    addIden(Id128Mtyp, 'BitId128')
    addIden(PyObjectMtyp, 'PyObject')
    
    def addSV(mtypClas, *typSV):
        fragr.symtab.mtypTriePutTypV([fragr.typStiFromStr(typS).child for typS in typSV], mtypClas)
        
    addSV(Id3v2EncodingMtyp, '/*id3v2Encoding*/ unsigned int')
    addSV(XUMtyp, '/*x*/ unsigned int')
    addSV(XU8Mtyp, '/*x*/ uint8_t')
    addSV(XU16Mtyp, '/*x*/ uint16_t')
    addSV(XU32Mtyp, '/*x*/ uint32_t')
    addSV(XU64Mtyp, '/*x*/ uint64_t')
    
    addSV(BMtyp, 'const uint8_t *', 'const uint8_t *')
    
    addSV(ZArrayMtyp, 'size_t []')
    
    #add(AufiETyp('aufiE', 'AufiE'))

    fragr.voidPtrSti = fragr.typStiFromStr('void *')
    fragr.pyObjectPtrSelfSti = fragr.typStiFromStr('PyObject *self')
    #fragr.symtab.mtypTriePutTypV((fragr.pyObjectPtrSelf.child,), PyObjectPtrMtyp)
    #todofragr.voidPtrMtyp = VoidPtrMtyp
    #addSV(VoidPtrMtyp, 'void *')
    #todofragr.pyObjectPtrMtyp = PyObjectPtrMtyp('pyoPtr')
    #fragr.symtab.mtypTriePutTypV((fragr.pyObjectPtrSelf.child,), PyObjectPtrMtyp)

    return fragr
