from . import ctyplib

def mfunBySigAddParamV(mfunBySig, paramV, fragr, funFromSig):
    # repace initial 'void *' arg with 'PyObject *self'
    if fragr.voidPtrSti.child is not paramV[0].child:
        raise Exception('voidPtr expected at paramV[0]')
    mtypV = [ ctyplib.PyObjectPtrMtyp((fragr.pyObjectPtrSelfSti.copy(),)) ]
    fragr.symtab.mtypVFromStiV(mtypV, paramV[1:], lambda sti: id(sti.child))
    sig = '_'.join([mtyp.Nick for mtyp in mtypV[1:]])
    if None is (mfun := mfunBySig.get(sig)):
        mfunBySig[sig] = mfun = CpyCbMfun(funFromSig(sig), mtypV)
    return mfun





def typeObjectCodeCpyH(iden):
    return f'''
extern PyTypeObject {iden}_PyType;

typedef struct {iden}_PyObject {{
	PyObject_HEAD
	{iden} kern;
}} {iden}_PyObject;

static inline {iden}*
{iden}_PyGetKern(PyObject *pyo) {{
    return PyObject_TypeCheck(pyo, &{iden}_PyType) ? &(({iden}_PyObject*)pyo)->kern : NULL;
}}
'''

#------------------------------------------------------------------------------------------------------------------------
# CpyCb
#------------------------------------------------------------------------------------------------------------------------

class CpyCbMfun:
    def __init__(self, iden, mtypV):
        self.iden = iden
        self.mtypV = mtypV
        
    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__}'):
            logr(f'[iden] {self.iden}')
            with logr(f'[mtypV]'):
                for mtyp in self.mtypV:
                    mtyp.dump(logr, '')

    def codeCpyH(self):
        return f'''
int {self.iden}({', '.join([sti.canon() for mtyp in self.mtypV for sti in mtyp.stiV])});
'''
    def codeCpyC(self):
        sep = ',\n    '
        return f'''
int {self.iden}({', '.join([sti.canon() for mtyp in self.mtypV for sti in mtyp.stiV])}) {{
    return PyObject_CallFunctionObjArgs(
        {sep.join([mtyp.pyObjCode(lambda sti: sti.iden) for mtyp in self.mtypV])},
        NULL) ? 0 : -1;
}}
'''


class CpyCbColl:
    def __init__(self):
        self.mfunBySig = {}

    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__}'):
            with logr(f'[mfunBySig]'):
                for sig,mfun in self.mfunBySig.items():
                    mfun.dump(logr, f'[{sig}] ')

    def addParamV(self, paramV, fragr, funFromSig):
        # repace initial 'void *' arg with 'PyObject *self'
        if fragr.voidPtrSti.child is not paramV[0].child:
            raise Exception('voidPtr expected at paramV[0]')
        mtypV = [ ctyplib.PyObjectPtrMtyp((fragr.pyObjectPtrSelfSti.copy(),)) ]
        fragr.symtab.mtypTrieMtypVFromStiV(mtypV, paramV[1:], lambda sti: id(sti.child))
        sig = '_'.join([mtyp.Nick for mtyp in mtypV[1:]])
        if None is (mfun := self.mfunBySig.get(sig)):
            self.mfunBySig[sig] = mfun = CpyCbMfun(funFromSig(sig), mtypV)
        return mfun

    def codeH(self): return ''
    def codeC(self): return ''
    
    def codeCpyH(self):
        return ''.join([mfun.codeCpyH() for mfun in self.mfunBySig.values()])
    
    def codeCpyC(self):
        return ''.join([mfun.codeCpyC() for mfun in self.mfunBySig.values()])
        
#------------------------------------------------------------------------------------------------------------------------
# CpyStruct
#------------------------------------------------------------------------------------------------------------------------

class CpyStruct:
    def __init__(self, iden, tp_name, initIden, stiV, fragr):
        self.iden = iden
        self.tp_name = tp_name
        self.initIden = initIden
        self.stiV = stiV
        # uniq1norm reduces arrays to the same regardless of size
        self.mtypV = fragr.symtab.mtypTrieMtypVFromStiV([], stiV, lambda sti: id(sti.child.uniq1Norm(fragr.symtab)))

    def codeH(self): return ''
    def codeC(self): return ''

    def codeCpyH(self):
        return typeObjectCodeCpyH(self.iden)

    def codeCpyC(self):
        fieldF = lambda sti: f'self->kern.{sti.iden}'
        getSetFuns = [self.codeCpyCGetFun(mtyp,fieldF) for mtyp in self.mtypV]
        getSetDefs = [self.codeCpyCGetDef(mtyp) for mtyp in self.mtypV]
        return f'''
static PyObject *
{self.iden}_PyNew(PyTypeObject *subtype, PyObject *args, PyObject *kwds)
{{
    {self.iden}_PyObject *self;
	
    if((self = ({self.iden}_PyObject*)subtype->tp_alloc(subtype, 0))) {{
        {self.initIden}(&self->kern);
        return (PyObject*)self;
    }}
    else PyErr_NoMemory();
    return NULL;
}}

static void
{self.iden}_PyDealloc({self.iden}_PyObject *self) 
{{
    PyObject_Del(self);
}}

{''.join(getSetFuns)}

PyGetSetDef {self.iden}_PyGetSetDefs[] = {{
{''.join(getSetDefs)}
    {{ NULL, NULL, NULL, NULL, NULL }}
}};

PyTypeObject {self.iden}_PyType = {{
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    .tp_name = "{self.tp_name}",
    .tp_basicsize = sizeof({self.iden}_PyObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor){self.iden}_PyDealloc,
    .tp_getset = {self.iden}_PyGetSetDefs,
    .tp_new = (newfunc){self.iden}_PyNew,
}};
'''

    def codeCpyCGetFun(self, mtyp, fieldF):
        return f'''
static PyObject *
{self.iden}_PyGet_{mtyp.stiV[0].iden}({self.iden}_PyObject *self, void *closure) {{
    return {mtyp.pyObjCode(fieldF)};
}}
'''

    def codeCpyCGetDef(self, mtyp):
        return f'''
    {{ "{mtyp.stiV[0].iden}", (getter){self.iden}_PyGet_{mtyp.stiV[0].iden}, NULL, NULL, NULL }},
'''

