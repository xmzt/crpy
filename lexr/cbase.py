import chtab

from pylib0_xmzt import enulib

#======================================================================================================================
# constants
#======================================================================================================================

PuncV = ('[ ] ( ) { } . -> '
         '++ -- & * + - ~ ! '
         '/ % << >> < > <= >= == != ^ | && || '
         '? : ; ... '
         '= *= /= %= += -= <<= >>= &= ^= |= '
         ', # ## '
         '<: :> <% %> %: %:%:').split()

#======================================================================================================================
# enums
#======================================================================================================================

AccTyp = enulib.Enu.create('AccTyp').addV('_0 u8 u U L'.split())
TokErr = enulib.Enu.create('TokErr').addV('BsEscapeInvalid QuotEof QuotEol'.split())
TokTyp = enulib.Enu.create('TokTyp').addV('Eof Other Ppn Cc Sl Iden'.split() + [chtab.name(punc) for punc in PuncV])
Ws = enulib.EnuBitmap.create('Ws').addV('H Eol Eof'.split())
