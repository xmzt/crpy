import clex

from pylib0_xmzt import loglib

import io
import re
import sys

class TestMismatchException(Exception): pass

TestSplitRe = re.compile(r'----\s*^', re.M)

testD = {}
testD['t0'] = r'''
01e-4
6 8[a]
auto
 _Thread_local
  u\
nionbu
----
    [tok] <1 1.0> [Eol] Ppn _0 '01e-4'
    [tok] <7 2.0> [Eol] Ppn _0 '6'
    [tok] <9 2.2> [H] Ppn _0 '8'
    [tok] <10 2.3> [0x0] Sbl
    [tok] <11 2.4> [0x0] Iden _0 'a'
    [tok] <12 2.5> [0x0] Sbr
    [tok] <14 3.0> [Eol] auto _0 'auto'
    [tok] <20 4.1> [H|Eol] _Thread_local _0 '_Thread_local'
    [tok] <36 5.2> [H|Eol] Iden _0 'unionbu'
    [tok] <46 7.0> [Eol|Eof] Eof
'''

testD['t1'] = r'''
.A
.0
..0
...0
----
    [tok] <1 1.0> [Eol] Dot
    [tok] <2 1.1> [Eol] Iden _0 'A'
    [tok] <4 2.0> [Eol] Ppn _0 '.0'
    [tok] <7 3.0> [Eol] Dot
    [tok] <8 3.1> [Eol] Ppn _0 '.0'
    [tok] <11 4.0> [Eol] Dot_Dot_Dot
    [tok] <14 4.3> [Eol] Ppn _0 '0'
    [tok] <16 5.0> [Eol|Eof] Eof
'''

testD['t2'] = r'''
.\
A
.\
0
.\
.\
0
.\
.\
.0
----
    [tok] <1 1.0> [Eol] Dot
    [tok] <4 2.0> [Eol] Iden _0 'A'
    [tok] <6 3.0> [Eol] Ppn _0 '.0'
    [tok] <11 5.0> [Eol] Dot
    [tok] <14 6.0> [Eol] Ppn _0 '.0'
    [tok] <19 8.0> [Eol] Dot_Dot_Dot
    [tok] <26 10.1> [Eol] Ppn _0 '0'
    [tok] <28 11.0> [Eol|Eof] Eof
'''

testD['t3'] = r'''
%\
:\
%\
A0.b
----
    [tok] <1 1.0> [Eol] Per_Col
    [tok] <7 3.0> [Eol] Per
    [tok] <10 4.0> [Eol] Iden _0 'A0'
    [tok] <12 4.2> [0x0] Dot
    [tok] <13 4.3> [0x0] Iden _0 'b'
    [tok] <15 5.0> [Eol|Eof] Eof
'''

testD['t4'] = r'''
ab\\
u\
3 c
4\u4567\u12\
abkl.4430
----
    [ERROR] <3 1.2> '\\\\\nu\\\n3' BsEscapeInvalid
    [tok] <1 1.0> [Eol] Iden _0 'ab\\u3'
    [tok] <11 3.2> [H] Iden _0 'c'
    [tok] <13 4.0> [Eol] Ppn _0 '4'
    [tok] <14 4.1> [0x0] Iden _0 '䕧ሁkl'
    [tok] <30 5.4> [0x0] Ppn _0 '.4430'
    [tok] <36 6.0> [Eol|Eof] Eof
'''

testD['t5'] = r'''
"abc\u3"
'4\u4567\u12\
abkl'
"a\a\b\t\n\v\f\r\0\0\
1\
7\
\\
x\
4\
1\"b"
'line
split'
'li----
    [ERROR] <5 1.4> '\\u3' BsEscapeInvalid
    [tok] <1 1.0> [Eol] Sl _0 'abc\\u3'
    [tok] <10 2.0> [Eol] Cc _0 '4䕧ሁkl'
    [tok] <30 4.0> [Eol] Sl _0 'a\x07\x08\t\n\x0b\x0c\r\x00\x0fA"b'
    [ERROR] <78 11.5> QuotEol
    [tok] <73 11.0> [Eol] Cc _0 'line\nsplit'
    [ERROR] <89 13.3> QuotEof
    [tok] <86 13.0> [Eol] Cc _0 'li'
    [tok] <89 13.3> [Eol|Eof] Eof
'''

logr = loglib.Logr5File()

class Logc(clex.Logc, loglib.Logc, metaclass=loglib.LogcMeta): pass
g_logc = clex.g_logc = clex.gen.g_logc = Logc().logrSet(logr).kvSet(
    ch=0, err=1, state=0, tok=1,
)

def parseFile(path):
    with open(sys.argv[1], 'r') as f:
        src = f.read() + '\0'
    with logr('src'):
        logr.mlPos(src)
    with logr('run'):
        clex.Parser().go(src, 0, clex.gen.START)

def parseTest(text):
    m = TestSplitRe.search(text)
    src,want = text[:m.start()] + '\0', text[m.end():]
    with logr('src'):
        logr.mlPos(src)
    with logr('run'):
        g_logc.logrSet(logr.birthFile2(sio := io.StringIO()))
        clex.Parser().go(src, 0, clex.gen.START)
    if (res := sio.getvalue()) != want:
        logr('[ERROR] result does not match expected')
        logr.ml(want)
        raise TestMismatchException()
    g_logc.logrSet(logr)

def parseTestAll():
    for text in testD.values():
        parseTest(text)
    
for arg in sys.argv[1:]:
    if 'all' == arg:
        parseTestAll()
    elif None is not (test := testD.get(arg)):
        parseTest(test)
    else:
        parsePath(arg)
