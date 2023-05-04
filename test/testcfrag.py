#!/usr/bin/python
#------------------------------------------------------------------------------------------------------------------------
# Usage
#
# ./testcfrag.py -p struct -dump
# ./testcfrag.py -s 'int x;' -dump
# ./testcfrag.py -f <file> -dump
#------------------------------------------------------------------------------------------------------------------------

import os
import sys
scriptDir = os.path.dirname(__file__)
sys.path[1:1] = [
    os.path.normpath(os.path.join(scriptDir, '../src/')),
    os.path.normpath(os.path.join(scriptDir, '../../pylib0/src')),
]

from crpy_xmzt import cpylib
from crpy_xmzt import castlib
from crpy_xmzt import cfraglib
from crpy_xmzt import ctyplib
from pylib0_xmzt import loglib,optslib

prefabs = { 'aufi':r'''
typedef int AufiApev2Cb_parseE(void *arg, int e, size_t pos);
typedef int AufiApev2Cb_head(void *arg,
							 size_t pos,
							 unsigned int version,
							 unsigned int size,
							 unsigned int itemsN,
							 unsigned int flags);
typedef int AufiApev2Cb_item(void *arg,
							 size_t pos,
							 unsigned int flags,
							 const uint8_t *key,
							 const uint8_t *keyE,
							 const uint8_t *val,
							 const uint8_t *valE);
typedef int AufiApev2Cb_foot(void *arg,
							 size_t pos,
							 unsigned int version,
							 unsigned int size,
							 unsigned int itemsN,
							 unsigned int flags);
typedef struct {
    size_t n;
    bong funk;
    size_t bitrateNs[AufiMpeg1AudFrameBitrateLayer3_Size];
    size_t frequencyNs[AufiMpeg1AudFrameFrequency_Size];
} AufiMpeg1AudFrameParseState;
''',
            'typedef':r'''
typedef int (*(*fun3ptr[3]  )(int a, unsigned b, long c))[2];
typedef AufiApev2Cb_parseE *a[2];
typedef AufiApev2Cb_parseE (*b)[2];
''',
            'struct':r'''
typedef struct {
	size_t n;
 	size_t bitrateNs[AufiMpeg1AudFrameBitrateLayer3_Size];
	size_t frequencyNs[AufiMpeg1AudFrameFrequency_Size];
} AufiMpeg1AudFrameParseState;

typedef struct ugga {
	//$! aufiGenr.parseCbsItemsFromFuns(dst, self.cbFuns)
	AufiMpeg1AudFrameParseCbs frame;
        AufiApev2ParseCbs apev2;
	AufiId3v1ParseCbs id3v1;
	AufiId3v2ParseCbs id3v2;
        /*x*/ const _Atomic(bungle*) /*AufiLyrics3v2ParseCbs*/ lyrics3v2 : 45;
} AufiMp3ParseCbs;
''',
            'enum':r'''
enum {
foo = 4,
bar,
huh = 3 5 6 23
} typedef dognasty;
enum named {
ghi = 3
} typedef chicken;
''',
            'prim':r'''
long x;
long long y;
long int long unsigned z;
''',
            'test0':r'''
long x;
''',
            'decl':r'''
typedef const int * a;
const a b = 4 5 6;
typedef static const int c;
volatile c * restrict d; 
int (*e)(a f, c *)[4];
typedef volatile _Atomic(a*restrict) f;
'''
}

class Main(optslib.Argr):
    def __init__(self):
        super().__init__(self)
        self.dumpUp = 0
        self.fragr = cfraglib.Fragr(specSlst=1)
        self.kvLog('fragr.logTok', 0, lambda tok,state: self.logr(f'[cfragTok] <{tok.pos}> {state} | {tok.typ.iden} {tok.val!r}'))
        self.kvLog('fragr.logStack', 0, lambda fragr: fragr.stackDump(self.logr, '[cfragStack] '))
        
    def opGo(self):
        self.logr = loglib.Logr5File()
        self.scope0 = ctyplib.initScope0(self.fragr)
        self.scope = self.scope0.dn()
        self.opGo = super().opGo
        self.opGo()
        
    def s(self, arg):
        self.fragr.goStart(self.scope, arg)

    def f(self, arg):
        with open(arg, 'r') as f:
            self.fragr.goStart(self.scope, f.read())

    def p(self, arg):
        self.fragr.goStart(self.scope, prefabs.get(arg))

    def typ(self, arg):
        sti = self.fragr.typFromStr(self.scope, arg)
        sti.dump(self.logr, '[sti] ')

    def dump(self):
        self.scope.dump(self.logr, '', self.dumpUp)

    def dumpCanon(self):
        self.scope.dumpCanon(self.logr, '', self.dumpUp)

    def cpycb(self):
        coll = cpylib.CpyCbColl(lambda sig: f'CB_{sig}')
        for k,sti in self.scope.items():
            if str is type(k) and sti.typP() and sti.child.funP():
                coll.addParamV(sti.child.paramV, self.fragr)
        coll.dump(self.logr, '[coll] ')
                
        print(coll.codeCpyH())
        print(coll.codeCpyC())

    def cpystruct(self):
        for k,sti in self.scope.items():
            if str is type(k) and sti.typP() and sti.child.structP():
                cpys = cpylib.CpyStruct('STRUCT', 'TP_NAME', 'STRUCT_INIT', sti.child.items, self.fragr)
                print(cpys.codeCpyC())
        
Main().argVGo(sys.argv[1:], 1)
