import clex

from pylib0_xmzt import loglib

import sys
import types

srcTest = types.SimpleNamespace()

srcTest.t0 = r'''
01e-4
6 8[a]
'''

srcTest.t1 = r'''
.A
.0
..0
...0
'''

srcTest.t2 = r'''
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
'''
#    [tok] <1 1.0>[Eol] Dot
#    [tok] <4 2.0>[Eol] Iden _0 'A'
#    [tok] <6 3.0>[Eol] Ppn _0 '.0'
#    [tok] <11 5.0>[Eol] Dot
#    [tok] <14 6.0>[Eol] Ppn _0 '.0'
#    [tok] <19 8.0>[Eol] Dot_Dot_Dot
#    [tok] <26 10.1>[Eol] Ppn _0 '0'
#    [tok] <28 11.0>[Eol|Eof] Eof

srcTest.t3 = r'''
%\
:\
%\
A0.b
'''

srcTest.t4 = r'''
ab\\
u\
3 c
4\u4567\u12\
abkl.4430
'''

srcTest.t5 = r'''
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
'li'''

logr = loglib.Logr5File()

class Logc(clex.Logc, loglib.Logc, metaclass=loglib.LogcMeta): pass
clex.g_logc = clex.gen.g_logc = Logc().logrSet(logr).kvSet(
    ch=0, err=1, state=0, tok=1,
)

for arg in sys.argv[1:]:
    if None is (src := getattr(srcTest, arg, None)):
        with open(sys.argv[1], 'r') as f:
            src = f.read()
    src += '\0'
    with logr('src'):
        logr.mlPos(src)
    with logr('run'):
        clex.Parser().go(src, 0, clex.gen.START)
