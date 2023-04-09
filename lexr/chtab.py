import itertools
import re

#======================================================================================================================
# table-less helpers
#======================================================================================================================

def patChars(patS):
    pat = re.compile(patS, re.S)
    return [ch for i in range(0, 0x0100) if pat.fullmatch(ch := chr(i))]

#======================================================================================================================
# build tables
#======================================================================================================================

quoteD = {}
nameD = {}
sym1D = {}

for i in range(0, 0x100):
    ch = chr(i)
    sym1D[ch] = quoteD[ch] = nameD[ch] = ch
    
for i in itertools.chain(range(0, 0x20), range(0x7F, 0x100)):
    n = nameD[ch := chr(i)] = 'x{0:02x}'.format(i)
    quoteD[ch] = f'\\{n}'
    sym1D[ch] = f'_{n}'

for ch,q,n in [ ( '\\', r'\\', 'Bsl' ),
                ( '\'', r'\'', 'Sq' ),
                ( '\"', r'\"', 'Dq' ),
                ( '\a', r'\a', 'Bel'),
                ( '\b', r'\b', 'Bsp' ),
                ( '\t', r'\t', 'Tab' ),
                ( '\n', r'\n', 'Nl'),
                ( '\v', r'\v', 'Vt' ),
                ( '\f', r'\f', 'Ff' ),
                ( '\r', r'\r', 'Cr' ) ]:
    quoteD[ch] = q
    nameD[ch] = n
    sym1D[ch] = f'_{n}'
    
for ch,n in [ ( ' ', 'Spa' ),
              ( '!', 'Exc' ),
              ( '#', 'Has' ),
              ( '$', 'Dol' ),
              ( '%', 'Per' ),
              ( '&', 'Amp' ),
              ( '(', 'Pl' ),
              ( ')', 'Pr' ),
              ( '*', 'Sta' ),
              ( '+', 'Plu' ),
              ( ',', 'Com' ),
              ( '-', 'Min' ),
              ( '.', 'Dot' ),
              ( '/', 'Sla' ),
              ( ':', 'Col' ),
              ( ';', 'Sem' ),
              ( '<', 'Lt' ),
              ( '=', 'Equ' ),
              ( '>', 'Gt' ),
              ( '?', 'Qm' ),
              ( '@', 'At' ),
              ( '[', 'Sbl' ),
              ( ']', 'Sbr' ),
              ( '^', 'Car' ),
              ( '_', 'Und' ),
              ( '`', 'Bti' ),
              ( '{', 'Cbl' ),
              ( '|', 'Bar' ),
              ( '}', 'Cbr' ),
              ( '~', 'Til' ) ]:
    nameD[ch] = n
    sym1D[ch] = f'_{n}'

symMD = sym1D.copy()
symMD['.'] = '.'
symMD['_'] = '_'

nameChD = {v:k for k,v in nameD.items()}
sym1ChD = {v:k for k,v in sym1D.items()}
symMChD = {v:k for k,v in symMD.items()}

#======================================================================================================================
# table helpers

def dump():
    for i in range(0, 0x100):
        ch = chr(i)
        print(f'{i:3d} 0x{i:02x} {quoteD[ch]:4s} {nameD[ch]:4s} {symD[ch]:4s}')
        
def quote1(x):
    return quoteD.get(x, x)

def quote(src):
    return ''.join([quoteD.get(x, x) for x in src])

def name1(x):
    return nameD.get(x, x)

def name(src):
    return '_'.join([nameD.get(x, x) for x in src])

def sym1(x):
    return sym1D.get(x, x)

def symM(src):
    return ''.join([symMD.get(x, x) for x in src])

def characterConstant(src):
    return f"'{quote(src)}'"

def stringLiteral(src):
    return f'"{quote(src)}"'

#wtf is this for? above should handle it
#def cQuote(src):
#    return re.sub(r'([\\\'\"])', r'\\\1', quote(src))
#def cCharQuoteTable():
#    return ',\n'.join([f'"{cQuote(chr(i))}"' for i in range(0,0x100)])

#======================================================================================================================
# chset

class ChsetNtermException(Exception): pass

def chsetDes(chV):
    orunA = -1
    orunE = -1
    accV = []
    def dump(orunA):
        if 2 < (orunE - orunA):
            accV.append(f'{chr(orunA)}-{chr(orunE-1)}')
        else:
            while orunA < orunE:
                accV.append(f'{chr(orunA)}')
                orunA += 1
            
    for ch in chV:
        if orunE != (o := ord(ch)):
            dump(orunA)
            orunA = o
        orunE = o + 1
    dump(orunA)
    return f'[{"".join(accV)!r}]'

ChsetParseRe = re.compile(r'(\\(?:[abtnvfr]|[0-9]{1,3}|x[0-9A-Fa-f]{1,2}))'
                          r'|(\\.)'
                          r'|(-)'
                          r'|(\])', re.S)

def chsetIadd(target, other):
    target.update(a)
    return target
    
def chsetIsub(target, other):
    for ch in other:
        try:
            del target[ch]
        except KeyError:
            pass
    return target

def chsetParse(chDset, src, pos):
    # divide into non-empty chunks separated at interpolating dashes
    chunkV = []
    chunk = []
    while None is not (m := ChsetParseRe.search(src, pos)):
        for x in src[pos:m.start()]:
            chunk.append(x)
        pos = m.end()
        if None is not (x := m.group(1)):
            chunk.append(eval(f"'''{x}'''"))
        elif None is not (x := m.group(2)):
            chunk.append(x[1])
        elif None is not m.group(3):
            if chunk:
                chunkV.append(chunk)
                chunk = []
            else:
                chunk.append('-')
        elif None is not m.group(4):
            if not chunk and chunkV:
                chunk.append('-')
            if chunk:
                chunkV.append(chunk)
            break
    else:
        raise ChsetNtermException()
    
    # combine chunks and interpolations
    interpA = 0
    for chunk in chunkV:
        if interpA:
            for x in range(interpA, ord(chunk[0])):
                chDset[chr(x)] = None
        for x in chunk:
            chDset[x] = None
        interpA = ord(chunk[-1]) + 1
    return pos

