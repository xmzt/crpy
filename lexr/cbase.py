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

KeywordV = ('_Alignas _Atomic auto _Bool char _Complex const double enum extern float inline int long _Noreturn'
            'register restrict short signed static struct _Thread_local typedef union unsigned void volatile').split()

#======================================================================================================================
# enums
#======================================================================================================================

AccTyp = enulib.Enu.create('AccTyp').addV('_0 u8 u U L'.split())
TokErr = enulib.Enu.create('TokErr').addV('BsEscapeInvalid QuotEof QuotEol'.split())
TokTyp = enulib.Enu.create('TokTyp').addV('Eof Other Ppn Cc Sl Iden'.split()
                                          + [chtab.name(punc) for punc in PuncV]
                                          + KeywordV)
TokTypByKeyword = {k:getattr(TokTyp, k) for k in KeywordV}
Ws = enulib.EnuBitmap.create('Ws').addV('H Eol Eof'.split())
