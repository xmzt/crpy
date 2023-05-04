from pylib0_xmzt.denumlib import Denum

import re 

#------------------------------------------------------------------------------------------------------------------------
# TokTyp
#------------------------------------------------------------------------------------------------------------------------

def TokTypMeta(name, bases, namespace, **kwds):
    cls = type(name, bases, namespace).init()
    for i,iden in enumerate((
        'Invalid',
        'Fin',
        # punctutation
        'BraceL',
        'BraceR',
        'BracketL',
        'BracketR',
        'Colon',
        'Comma',
        'Eq',
        'Hash',
        'ParenL',
        'ParenR',
        'Semi',
        'Star',
        # keyword
        'Alignas',
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
        'Inline',
        'Int',
        'Long',
        'Noreturn',
        'Register',
        'Restrict',
        'Short',
        'Signed',
        'Static',
        'Struct',
        'ThreadLocal',
        'Typedef',
        'Union',
        'Unsigned',
        'Void',
        'Volatile',
        # with values
        'Iden',
        'Slsl',
        'Slst',
    )):
        cls.add(iden, i-1, -1)
    cls.Order = cls.order(cls.ItemV[-1].val)
    return cls
    
class TokTyp(Denum, metaclass=TokTypMeta): pass

#------------------------------------------------------------------------------------------------------------------------
# Tok
#------------------------------------------------------------------------------------------------------------------------

class Tok:
    TypByReGroup1 = {
        '{': TokTyp.BraceL,
        '}': TokTyp.BraceR,
        '[': TokTyp.BracketL,
        ']': TokTyp.BracketR,
        ':': TokTyp.Colon,
        ',': TokTyp.Comma,
        '=': TokTyp.Eq,
        '#': TokTyp.Hash,
        '(': TokTyp.ParenL,
        ')': TokTyp.ParenR,
        ';': TokTyp.Semi,
        '*': TokTyp.Star,
    }

    TypByReGroup2 = {
        '_Alignas':      TokTyp.Alignas,
        '_Atomic':       TokTyp.Atomic,
        'auto':          TokTyp.Auto,
        '_Bool':         TokTyp.Bool,
        'char':          TokTyp.Char,
        '_Complex':      TokTyp.Complex,
        'const':         TokTyp.Const,
        'double':        TokTyp.Double,
        'enum':          TokTyp.Enum,
        'extern':        TokTyp.Extern,
        'float':         TokTyp.Float,
        'inline':        TokTyp.Inline,
        'int':           TokTyp.Int,
        'long':          TokTyp.Long,
        '_Noreturn':     TokTyp.Noreturn,
        'register':      TokTyp.Register,
        'restrict':      TokTyp.Restrict,
        'short':         TokTyp.Short,
        'signed':        TokTyp.Signed,
        'static':        TokTyp.Static,
        'struct':        TokTyp.Struct,
        '_Thread_local': TokTyp.ThreadLocal,
        'typedef':       TokTyp.Typedef,
        'union':         TokTyp.Union,
        'unsigned':      TokTyp.Unsigned,
        'void':          TokTyp.Void,
        'volatile':      TokTyp.Volatile,
    }

    def __init__(self, pos, typ, val):
        self.pos = pos
        self.typ = typ
        self.val = val
    
    Re = re.compile(r'\s*(([{}\[\]:,=#();*])|(\w+)|(/\*.*?\*/)|(//(?m:.*?$))|$)', re.S)

    @classmethod
    def fromReMatch(cls, m):
        if None is not (val := m.group(2)):
            typ = cls.TypByReGroup1[val]
        elif None is not (val := m.group(3)):
            typ = cls.TypByReGroup2.get(val, TokTyp.Iden)
        elif None is not (val := m.group(4)):
            typ = TokTyp.Slst
        elif None is not (val := m.group(5)):
            typ = TokTyp.Slsl
        else:
            typ = TokTyp.Fin
            val = None
        return cls(m.start(1), typ, val)
