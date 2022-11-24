from . import castlib
from .ctoklib import Tok,TokTyp

import re 

#------------------------------------------------------------------------------------------------------------------------
# Exceptions
#------------------------------------------------------------------------------------------------------------------------

class CfragException(Exception): pass
class SpecInvalidException(CfragException): pass
class TokInvalidException(CfragException): pass
class TokUnexpectedException(CfragException): pass
class TokUnmatchedException(CfragException): pass
class TypExpectedException(CfragException): pass
class TypedefUnexpectedException(CfragException): pass
class RatorIdenExpectedException(CfragException): pass
class RatorIdenUnexpectedException(CfragException): pass

#------------------------------------------------------------------------------------------------------------------------
# StackFrame
#------------------------------------------------------------------------------------------------------------------------

class StackFrame:
    def __init__(self, up, kwargs):
        self.up = up
        self.__dict__.update(kwargs)

    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__}'):
            for k,v in self.__dict__.items():
                if None is not (d := getattr(v, 'dump', None)):
                    d(logr, f'[{k}] ')
                else:
                    logr(f'[{k}] {v!r}')

#------------------------------------------------------------------------------------------------------------------------
# Fragr
#------------------------------------------------------------------------------------------------------------------------

class Fragr:
    StateV = ('blob',
              'enumBraceL',
              'enumBraceLIden',
              'enumBraceLIdenEqInitr',
              'fin',
              'paramList',
              'paramListRator',
              'rator',
              'ratorParenL',
              'ratorRoot',
              'ratorStar',
              'spec',
              'specAlignas',
              'specAtomic',
              'specAtomicParenLRator',
              'specEnum',
              'specEnumIden',
              'specStruct',
              'specStructIden',
              'specUnion',
              'specUnionIden',
              'start',
              'startTyp',
              'startTypRator',
              'suBraceL',
              'suBraceLRator',
              'suBraceLRatorColonBitfield',
              'topDeclRator',
              'topDeclRatorEqInitr')

    SpecTokTypV = ('Alignas',
                   'Atomic',
                   'Auto',
                   'Bool',
                   'Char',
                   'Complex',
                   'Const',
                   'Double',
                   'Enum',
                   'Extern',
                   'Float',
                   'Iden',
                   'Inline',
                   'Int',
                   'Long',
                   'Noreturn',
                   'Register',
                   'Restrict',
                   'Short',
                   'Signed',
                   'Slst',
                   'Static',
                   'Struct',
                   'ThreadLocal',
                   'Typedef',
                   'Union',
                   'Unsigned',
                   'Void',
                   'Volatile')

    def __init__(self, symtab):
        #externally defined
        #spec.specSlst

        self.symtab = symtab

    def logTok(self, tok, state): pass
    def logStack(self, fragr): pass

    def goSrc(self, src):
        i = 0
        while 'fin' != self.state:
            if None is (m := Tok.Re.match(src, i)):
                raise TokInvalidException(i)
            i = m.end(0)
            self.tok = Tok.fromReMatch(m)
            self.tokGo()

    def goStart(self, src):
        self.startCall()
        self.goSrc(src)

    def goStartScopeNew0(self, src):
        scope = self.symtab.scopeSetNew0()
        self.goStart(src)
        return scope
        
    def typStiFromStr(self, src):
        self.startTypCall()
        self.goSrc(src)
        return self.result

    def stackDump(self, logr, pre):
        if None is self.stack:
            logr(f'{pre}None')
        else:
            self.stack.dump(logr, pre)

    #--------------------------------------------------------------------------------------------------------------------
    # parse helpers

    def stackPush(self, **kwargs):
        self.stack = StackFrame(self.stack, kwargs)

    def stackPushRet(self, ret, **kwargs):
        self.stack = StackFrame(self.stack, kwargs)
        self.stack.ret = ret

    def stackPop(self, *args):
        self.stack = self.stack.up

    def stackPopRet(self, *args):
        ret = self.stack.ret
        self.stack = self.stack.up
        ret(*args)

    def tokGo(self):
        self.logTok(self.tok, self.state)
        self.logStack(self)
        if None is (meth := getattr(self, '_'.join(('sm', self.state, self.tok.typ.iden)), None)):
            if None is (meth := getattr(self, '_'.join(('sm', self.state, '_other')), None)):
                raise TokUnexpectedException(self.tok.pos)
        meth()
        
    def sm_noop(self): pass

    #--------------------------------------------------------------------------------------------------------------------
    # blob
    #
    # RETURN list of toks; self.tok consumed
    #
    # STACK (ret, list_of_toks, stack_of_sets)
    #
    # note: add 1 to self.tok.typ when pushing on stack so that it will match the ...R version of a ...L tok

    def blobCall(self, ret, *args):
        self.stackPushRet(ret, toks=[], setStack=[set([arg.val for arg in args])])
        self.state = 'blob'
        
    def sm_blob__other(self):
        if self.tok.typ in self.stack.setStack[-1]:
            self.stack.setStack.pop()
            if not self.stack.setStack:
                return self.stackPopRet(self.stack.toks)
        self.stack.toks.append(self.tok)
        
    def sm_blob_BraceL(self):
        self.stack.setStack.append(set([self.tok.typ.val + 1]))
        self.stack.toks.append(self.tok)
        
    sm_blob_BracketL = sm_blob_BraceL
    sm_blob_ParenL = sm_blob_BraceL
        
    def sm_blob_BraceR(self):
        if self.tok.typ not in self.stack.setStack.pop():
            raise TokUnmatchedException(self.tok.pos)
        if not self.stack.setStack:
            return self.stackPopRet(self.stack.toks)
        self.stack.toks.append(self.tok)

    sm_blob_BracketR = sm_blob_BraceR
    sm_blob_ParenR = sm_blob_BraceR
        
    #--------------------------------------------------------------------------------------------------------------------
    # rator 
    #
    # RETURN (rev=[reverse order list of Typ segments]); self.tok unconsumed
    #
    # some trickiness with stack frames
    #
    # --------------------------------------------------
    # ratorRoot

    def ratorCall(self, ret):
        self.stackPushRet(ret, rev=None)
        self.state = 'rator'

    # --------------------------------------------------
    # rator state 'rator'

    def sm_rator__other(self):
        # return anon_root
        self.stackPopRet(castlib.SymtabItem(None, None, self.tok.pos))
        
    def sm_rator_BracketL(self):
        # set to array,anon_root
        self.stack.rev = castlib.TypArray(castlib.SymtabItem(None, None, self.tok.pos), None)
        self.blobCall(self.ratorRootBracketLRet, TokTyp.BracketR)

    def sm_rator_Iden(self):
        # set to named_root
        self.stack.rev = castlib.SymtabItem(self.tok.val, None, self.tok.pos)
        self.state = 'ratorRoot'

    def sm_rator_ParenL(self):
        self.stackPushRet(self.ratorParenLRet, rev=None, tmpPos=self.tok.pos)
        self.state = 'ratorParenL'

    def sm_rator_Star(self):
        # add flags to current frame before adding new frame
        self.stack.flags = 0
        self.stackPushRet(self.ratorStarRet, rev=None)
        self.state = 'ratorStar'

    # --------------------------------------------------
    # rator state 'ratorParenL'

    sm_ratorParenL_BracketL = sm_rator_BracketL

    def sm_ratorParenL_Iden(self):
        # todo does this need to match any tok that might start a spec?
        if None is not (sti := self.symtab.get(self.tok.val)) and sti.typP():
            # fun with empty root
            self.stack.rev = castlib.TypFun(castlib.SymtabItem(None, None, self.stack.tmpPos))
            self.paramListCall(self.ratorRoot__other, self.stack.rev) # ratorRootOther pops next stack frame
            self.tokGo()
        else:
            self.sm_rator_Iden()

    sm_ratorParenL_ParenL = sm_rator_ParenL
        
    def sm_ratorParenL_ParenR(self):
        # return anon_root
        self.stackPopRet(castlib.SymtabItem(None, None, self.stack.tmpPos))

    sm_ratorParenL_Star = sm_rator_Star
        
    def ratorParenLRet(self, rev):
        if TokTyp.ParenR != self.tok.typ:
            raise TokUnexpectedException(self.tok.pos)
        self.stack.rev = rev
        self.state = 'ratorRoot'

    # --------------------------------------------------
    # rator state 'ratorRoot'

    def sm_ratorRoot__other(self):
        self.stackPopRet(self.stack.rev)

    def sm_ratorRoot_ParenL(self):
        # prepend fun
        self.stack.rev = castlib.TypFun(self.stack.rev)
        self.paramListCall(self.ratorRootParenLRet, self.stack.rev)

    def ratorRootParenLRet(self):
        self.state = 'ratorRoot'

    def sm_ratorRoot_BracketL(self):
        # prepend array
        self.stack.rev = castlib.TypArray(self.stack.rev, None)
        self.blobCall(self.ratorRootBracketLRet, TokTyp.BracketR)

    def ratorRootBracketLRet(self, toks):
        self.stack.rev.toks = toks
        self.state = 'ratorRoot'

    # --------------------------------------------------
    # rator state 'ratorStar'

    sm_ratorStar__other = sm_rator__other

    sm_ratorStar_Iden = sm_rator_Iden

    sm_ratorStar_BracketL = sm_rator_BracketL

    sm_ratorStar_ParenL = sm_rator_ParenL

    def sm_ratorStar_Atomic(self):
        self.stack.up.flags |= castlib.SpecFlag.TypQualAtomic
        self.state = 'ratorStar'
        
    def sm_ratorStar_Const(self):
        self.stack.up.flags |= castlib.SpecFlag.TypQualConst
        self.state = 'ratorStar'
        
    def sm_ratorStar_Restrict(self):
        self.stack.up.flags |= castlib.SpecFlag.TypQualRestrict
        self.state = 'ratorStar'
        
    def sm_ratorStar_Volatile(self):
        self.stack.up.flags |= castlib.SpecFlag.TypQualVolatile
        self.state = 'ratorStar'

    def ratorStarRet(self, rev):
        if self.stack.flags:
            rev = castlib.TypMod(rev, self.stack.flags)
        self.stackPopRet(castlib.TypPtr(rev))
            
    #--------------------------------------------------------------------------------------------------------------------
    # spec
    #
    # RETURN (spec); self.tok unconsumed

    def specCall0(self, ret):
        self.stackPushRet(ret, spec=castlib.ParseSpec())
        self.state = 'spec'

    def specCall(self, ret, specFun):
        self.stackPushRet(ret, spec=castlib.ParseSpec())
        specFun()

    def sm_spec__other(self):
        if not (castlib.SpecFlag.TypSpecNprimitive & self.stack.spec.flags):
            if None is (sti := self.symtab.primGet(castlib.SpecFlag.TypSpecMask & self.stack.spec.flags)):
                raise SpecInvalidException(self.tok.pos)
            self.stack.spec.child = sti.child

        # extract TypQual flags
        if (qualFlags := castlib.SpecFlag.TypQualMask & self.stack.spec.flags):
            self.stack.spec.child = castlib.TypMod(self.stack.spec.child, qualFlags).uniq1(self.symtab)

        self.stackPopRet(self.stack.spec)
            
    def sm_spec_Alignas(self):
        self.state = 'specAlignas'

    def sm_spec_Atomic(self):
        self.state = 'specAtomic'

    def sm_spec_Enum(self):
        if castlib.SpecFlag.TypSpecMask & self.stack.spec.flags:
            raise SpecInvalidException(self.tok.pos)
        self.stack.spec.flags |= castlib.SpecFlag.TypSpecNprimitive
        self.stack.tmpPos = self.tok.pos
        self.state = 'specEnum'

    def sm_spec_Iden(self):
        if castlib.SpecFlag.TypSpecMask & self.stack.spec.flags:
            self.sm_spec__other()
        else:
            if None is (sti := self.symtab.get(self.tok.val)):
                sti = self.symtab.idenPut(castlib.TypUnknown(self.tok.val), self.tok.pos)
            elif not sti.typP():
                raise TypExpectedException(self.tok.pos)
            
            sti.child.parseSpecFromThis(self.stack.spec, self.symtab)
            self.stack.spec.flags |= castlib.SpecFlag.TypSpecNprimitive 
            self.state = 'spec'

    def sm_spec_Struct(self):
        if castlib.SpecFlag.TypSpecMask & self.stack.spec.flags:
            raise SpecInvalidException(self.tok.pos)
        self.stack.spec.flags |= castlib.SpecFlag.TypSpecNprimitive
        self.stack.tmpPos = self.tok.pos
        self.state = 'specStruct'

    def sm_spec_Union(self):
        if castlib.SpecFlag.TypSpecMask & self.stack.spec.flags:
            raise SpecInvalidException(self.tok.pos)
        self.stack.spec.flags |= castlib.SpecFlag.TypSpecNprimitive
        self.stack.tmpPos = self.tok.pos
        self.state = 'specUnion'

    #-------------------------------------------------------------
    # spec flags 

    def specFlag(self, flags):
        self.stack.spec.flags |= flags
        self.state = 'spec'

    def specFlagPrimitive(self, flags):
        if castlib.SpecFlag.TypSpecNprimitive & self.stack.spec.flags:
            raise SpecInvalidException(self.tok.pos)
        self.stack.spec.flags |= flags
        self.state = 'spec'
        
    def sm_spec_Auto(self):        self.specFlag         (castlib.SpecFlag.StorageClasAuto)
    def sm_spec_Bool(self):        self.specFlagPrimitive(castlib.SpecFlag.TypSpecBool)
    def sm_spec_Char(self):        self.specFlagPrimitive(castlib.SpecFlag.TypSpecChar)
    def sm_spec_Complex(self):     self.specFlagPrimitive(castlib.SpecFlag.TypSpecComplex)
    def sm_spec_Const(self):       self.specFlag         (castlib.SpecFlag.TypQualConst)
    def sm_spec_Double(self):      self.specFlagPrimitive(castlib.SpecFlag.TypSpecDouble)
    def sm_spec_Extern(self):      self.specFlag         (castlib.SpecFlag.StorageClasExtern)
    def sm_spec_Float(self):       self.specFlagPrimitive(castlib.SpecFlag.TypSpecFloat)
    def sm_spec_Inline(self):      self.specFlag         (castlib.SpecFlag.FunSpecInline)
    def sm_spec_Int(self):         self.specFlagPrimitive(castlib.SpecFlag.TypSpecInt)
    def sm_spec_Noreturn(self):    self.specFlag         (castlib.SpecFlag.FunSpecNoreturn)
    def sm_spec_Register(self):    self.specFlag         (castlib.SpecFlag.StorageClasRegister)
    def sm_spec_Restrict(self):    self.specFlag         (castlib.SpecFlag.TypQualRestrict)
    def sm_spec_Short(self):       self.specFlagPrimitive(castlib.SpecFlag.TypSpecShort)
    def sm_spec_Signed(self):      self.specFlagPrimitive(castlib.SpecFlag.TypSpecSigned)
    def sm_spec_Static(self):      self.specFlag         (castlib.SpecFlag.StorageClasStatic)
    def sm_spec_ThreadLocal(self): self.specFlag         (castlib.SpecFlag.StorageClasThreadLocal)
    def sm_spec_Typedef(self):     self.specFlag         (castlib.SpecFlag.StorageClasTypedef)
    def sm_spec_Unsigned(self):    self.specFlagPrimitive(castlib.SpecFlag.TypSpecUnsigned)
    def sm_spec_Void(self):        self.specFlagPrimitive(castlib.SpecFlag.TypSpecVoid)
    def sm_spec_Volatile(self):    self.specFlag         (castlib.SpecFlag.TypQualVolatile)

    def sm_spec_Long(self):
        if castlib.SpecFlag.TypSpecNprimitive & self.stack.spec.flags:
            raise SpecInvalidException(self.tok.pos)
        if castlib.SpecFlag.TypSpecLong1 & self.stack.spec.flags:
            if castlib.SpecFlag.TypSpecLong2 & self.stack.spec.flags:
                raise SpecInvalidException(self.tok.pos)
            else:
                self.stack.spec.flags |= castlib.SpecFlag.TypSpecLong2
        else:
            self.stack.spec.flags |= castlib.SpecFlag.TypSpecLong1
            
            
        self.state = 'spec'
        
    def sm_spec_Slst(self):       
        if self.specSlst:
            if '/*x*/' == self.tok.val:
                self.stack.spec.flags |= castlib.SpecFlag.TypQualSlstHex
            elif '/*id3v2Encoding*/' == self.tok.val:
                self.stack.spec.flags |= castlib.SpecFlag.TypQualSlstId3v2Encoding
        self.state = 'spec'

    #-------------------------------------------------------------
    # specAlignas

    def sm_specAlignas_ParenL(self):
        self.blobCall(self.specAlignasParenLRet, TokTyp.ParenR)

    def specAlignasParenLRet(self, toks):
        self.stack.spec.alignas = toks
        self.state = 'spec'

    #-------------------------------------------------------------
    # specAtomic

    def sm_specAtomic__other(self):
        self.stack.spec.flags |= castlib.SpecFlag.TypQualAtomic
        self.state = 'spec'
        self.tokGo()

    def sm_specAtomic_ParenL(self):
        if castlib.SpecFlag.TypSpecMask & self.stack.spec.flags:
            raise SpecInvalidException(self.tok.pos)
        self.stack.spec.flags |= castlib.SpecFlag.TypSpecNprimitive
        self.specCall0(self.specAtomicParenLSpecRet)

    def specAtomicParenLSpecRet(self, spec):
        self.stack.tmpAtomicSpec = spec
        self.ratorCall(self.specAtomicParenLRatorRet)
        self.tokGo()

    def specAtomicParenLRatorRet(self, rev):
        self.stack.spec.child = self.stack.tmpAtomicSpec.ratorRevStiUniq(self.symtab, rev).toAtomic(self.stack.tmpAtomicSpec)
        self.state = 'specAtomicParenLRator'
        self.tokGo()

    def sm_specAtomicParenLRator_ParenR(self):
        self.state = 'spec'

    #-------------------------------------------------------------
    # specEnum
        
    def sm_specEnum_BraceL(self):
        self.stack.tmpSti = self.symtab.enumNewAnon()
        self.stack.tmpSti.pos = self.stack.tmpPos
        self.stack.spec.child = self.stack.tmpSti.child
        self.stack.spec.child.itemsInit()
        self.enumBraceLCall(self.specEnumIdenBraceLRet, self.stack.spec.child)

    def sm_specEnum_Iden(self):
        self.stack.tmpSti = self.symtab.enumGetOrNew(self.tok.val)
        self.stack.spec.child = self.stack.tmpSti.child
        self.state = 'specEnumIden'
        
    sm_specEnumIden__other = sm_spec__other

    def sm_specEnumIden_BraceL(self):
        self.stack.tmpSti.pos = self.stack.tmpPos
        self.stack.spec.child.itemsInit()
        self.enumBraceLCall(self.specEnumIdenBraceLRet, self.stack.spec.child)

    def specEnumIdenBraceLRet(self):
        self.state = 'spec'

    for k in SpecTokTypV:
        exec(f'sm_specEnumIden_{k} = sm_spec_{k}')

    #-------------------------------------------------------------
    # specStruct

    def sm_specStruct_BraceL(self):
        self.stack.tmpSti = self.symtab.structNewAnon()
        self.stack.tmpSti.pos = self.stack.tmpPos
        self.stack.spec.child = self.stack.tmpSti.child
        self.stack.spec.child.itemsInit()
        self.suBraceLCall(self.specStructIdenBraceLRet, self.stack.spec.child)
        
    def sm_specStruct_Iden(self):
        self.stack.tmpSti = self.symtab.structGetOrNew(self.tok.val)
        self.stack.spec.child = self.stack.tmpSti.child
        self.state = 'specStructIden'

    sm_specStructIden__other = sm_spec__other

    def sm_specStructIden_BraceL(self):
        self.stack.tmpSti.pos = self.stack.tmpPos
        self.stack.spec.child.itemsInit()
        self.suBraceLCall(self.specStructIdenBraceLRet, self.stack.spec.child)

    def specStructIdenBraceLRet(self):
        self.state = 'spec'

    for k in SpecTokTypV:
        exec(f'sm_specStructIden_{k} = sm_spec_{k}')

    #-------------------------------------------------------------
    # specUnion

    def sm_specUnion_BraceL(self):
        self.stack.tmpSti = self.symtab.unionNewAnon()
        self.stack.tmpSti.pos = self.stack.tmpPos
        self.stack.spec.child = self.stack.tmpSti.child
        self.stack.spec.child.itemsInit()
        self.suBraceLCall(self.specUnionIdenBraceLRet, self.stack.spec.child)
        
    def sm_specUnion_Iden(self):
        self.stack.tmpSti = self.symtab.unionGetOrNew(self.tok.val)
        self.stack.spec.child = self.stack.tmpSti.child
        self.state = 'specUnionIden'

    sm_specUnionIden__other = sm_spec__other

    def sm_specUnionIden_BraceL(self):
        self.stack.tmpSti.pos = self.stack.tmpPos
        self.stack.spec.child.itemsInit()
        self.suBraceLCall(self.specUnionIdenBraceLRet, self.stack.spec.child)

    def specUnionIdenBraceLRet(self):
        self.state = 'spec'

    for k in SpecTokTypV:
        exec(f'sm_specUnionIden_{k} = sm_spec_{k}')

    #--------------------------------------------------------------------------------------------------------------------
    # enumBraceL
    #
    # RETURN nothing, self.tok consumed
    #
    # STACK (ret, initr, iden, pos, typ)

    def enumBraceLCall(self, ret, typ):
        self.stackPushRet(ret, typ=typ)
        self.state = 'enumBraceL'
        
    def sm_enumBraceL_BraceR(self):
        self.stackPopRet()

    def sm_enumBraceL_Iden(self):
        self.stack.iden = self.tok.val
        self.stack.tmpPos = self.tok.pos
        self.state = 'enumBraceLIden'

    def sm_enumBraceLIden_Eq(self):
        self.blobCall(self.enumBraceLIdenEqInitrRet, TokTyp.BraceR, TokTyp.Comma)

    def enumBraceLIdenEqInitrRet(self, toks):
        self.stack.initr = toks
        self.state = 'enumBraceLIdenEqInitr'
        self.tokGo()

    def sm_enumBraceLIdenEqInitr_Comma(self):
        self.stack.typ.itemAdd(castlib.SymtabItemInitr(self.stack.iden, None, self.stack.tmpPos, self.stack.initr))
        self.state = 'enumBraceL'

    def sm_enumBraceLIdenEqInitr_BraceR(self):
        self.stack.typ.itemAdd(castlib.SymtabItemInitr(self.stack.iden, None, self.stack.tmpPos, self.stack.initr))
        self.stackPopRet()

    def sm_enumBraceLIden_Comma(self):
        self.stack.typ.itemAdd(castlib.SymtabItem(self.stack.iden, None, self.stack.tmpPos))
        self.state = 'enumBraceL'

    def sm_enumBraceLIden_BraceR(self):
        self.stack.typ.itemAdd(castlib.SymtabItem(self.stack.iden, None, self.stack.tmpPos))
        self.stackPopRet()

    #--------------------------------------------------------------------------------------------------------------------
    # suBraceL [struct or union]
    #
    # RETURN list of rations, self.tok consumed

    def suBraceLCall(self, ret, typ):
        self.stackPushRet(ret, typ=typ)
        self.state = 'suBraceL'

    def sm_suBraceL_BraceR(self):
        self.stackPopRet()

    for k in SpecTokTypV:
        exec(f'def sm_suBraceL_{k}(self): self.specCall(self.suBraceLSpecRet, self.sm_spec_{k})')

    def suBraceLSpecRet(self, spec):
        self.stack.spec = spec
        self.ratorCall(self.suBraceLRatorRet)
        self.tokGo()
        
    def suBraceLRatorRet(self, rev):
        self.stack.sti = self.stack.spec.ratorRevStiUniq(self.symtab, rev)
        self.state = 'suBraceLRator'
        self.tokGo()

    def sm_suBraceLRator_Colon(self):
        self.blobCall(self.suBraceLRatorColonBitfieldRet, TokTyp.Comma, TokTyp.Semi)

    def suBraceLRatorColonBitfieldRet(self, toks):
        self.stack.bitfield = toks
        self.state = 'suBraceLRatorColonBitfield'
        self.tokGo()
        
    def sm_suBraceLRatorColonBitfield_Comma(self):
        self.stack.typ.itemAdd(self.stack.sti.toDeclBitfield(self.stack.spec, self.stack.bitfield))
        self.ratorCall(self.suBraceLRatorRet)

    def sm_suBraceLRatorColonBitfield_Semi(self):
        self.stack.typ.itemAdd(self.stack.sti.toDeclBitfield(self.stack.spec, self.stack.bitfield))
        self.state = 'suBraceL'

    def sm_suBraceLRator_Comma(self):
        self.stack.typ.itemAdd(self.stack.sti.toDecl(self.stack.spec))
        self.ratorCall(self.suBraceLRatorRet)

    def sm_suBraceLRator_Semi(self):
        self.stack.typ.itemAdd(self.stack.sti.toDecl(self.stack.spec))
        self.state = 'suBraceL'

    #--------------------------------------------------------------------------------------------------------------------
    # paramList (paramater list as in a function declaration)
    #
    # RETURN nothing, self.tok consumed

    def paramListCall(self, ret, typ):
        self.stackPushRet(ret, typ=typ)
        self.state = 'paramList'

    def sm_paramList_ParenR(self):
        self.stackPopRet()
        
    for k in SpecTokTypV:
        exec(f'def sm_paramList_{k}(self): self.specCall(self.paramListSpecRet, self.sm_spec_{k})')

    def paramListSpecRet(self, spec):
        self.stack.spec = spec
        self.ratorCall(self.paramListRatorRet)
        self.tokGo()

    def paramListRatorRet(self, rev):
        self.stack.typ.paramAdd(self.stack.spec.ratorRevStiUniq(self.symtab, rev).toParam(self.stack.spec))
        self.state = 'paramListRator'
        self.tokGo()

    def sm_paramListRator_Comma(self):
        self.state = 'paramList'

    sm_paramListRator_ParenR = sm_paramList_ParenR
        
    #--------------------------------------------------------------------------------------------------------------------
    # topDecl
    #
    # RETURN list of rations, self.tok consumed

    def topDeclCall(self, ret, specFun):
        self.stackPushRet(ret) 
        self.specCall(self.topDeclSpecRet, specFun)
        
    def topDeclSpecRet(self, spec):
        self.stack.spec = spec
        self.ratorCall(self.topDeclRatorRet)
        self.tokGo()

    def topDeclRatorRet(self, rev):
        self.stack.sti = self.stack.spec.ratorRevStiUniq(self.symtab, rev)
        self.state = 'topDeclRator'
        self.tokGo()

    def sm_topDeclRator_Comma(self):
        self.symtab.itemPut(self.stack.sti.toDecl(self.stack.spec))
        self.ratorCall(self.topDeclRatorRet)
        
    def sm_topDeclRator_Eq(self):
        self.blobCall(self.topDeclRatorEqInitrRet, TokTyp.Comma, TokTyp.Semi)
        
    def topDeclRatorEqInitrRet(self, toks):
        self.stack.initr = toks
        self.state = 'topDeclRatorEqInitr'
        self.tokGo()
        
    def sm_topDeclRatorEqInitr_Semi(self):
        self.symtab.itemPut(self.stack.sti.toDeclInitr(self.stack.spec, self.stack.initr))
        self.stackPopRet()
        
    def sm_topDeclRatorEqInitr_Comma(self):
        self.symtab.itemPut(self.stack.sti.toDeclInitr(self.stack.spec, self.stack.initr))
        self.ratorCall(self.topDeclRatorRet)
        
    def sm_topDeclRator_Semi(self):
        self.symtab.itemPut(self.stack.sti.toDecl(self.stack.spec))
        self.stackPopRet()

    #--------------------------------------------------------------------------------------------------------------------
    # start

    def startCall(self):
        self.stack = None
        self.state = 'start'

    def sm_start_Fin(self):
        self.state = 'fin'

    for k in SpecTokTypV:
        exec(f'def sm_start_{k}(self): self.topDeclCall(self.startTopDeclRet, self.sm_spec_{k})')
        
    def startTopDeclRet(self):
        self.state = 'start'

    #--------------------------------------------------------------------------------------------------------------------
    # startTyp

    def startTypCall(self):
        self.result = None
        self.stack = None
        self.stackPush()
        self.state = 'startTyp'

    def sm_startTyp_Fin(self):
        self.state = 'fin'
        self.result = self.stack.sti
        self.stackPop()

    for k in SpecTokTypV:
        exec(f'def sm_startTyp_{k}(self): self.specCall(self.startTypSpecRet, self.sm_spec_{k})')
        
    def startTypSpecRet(self, spec):
        self.stack.spec = spec
        self.ratorCall(self.startTypRatorRet)
        self.tokGo()

    def startTypRatorRet(self, rev):
        self.stack.sti = self.stack.spec.ratorRevStiUniq(self.symtab, rev)
        self.state = 'startTypRator'
        self.tokGo()

    sm_startTypRator_Fin = sm_startTyp_Fin

    #--------------------------------------------------------------------------------------------------------------------
    # comments

    locs = locals()
    for state in StateV:
        for k in (f'sm_{state}_Slsl', f'sm_{state}_Slst'):
            if k not in locs:
                exec(f'{k} = sm_noop')
    del locs, state, k
