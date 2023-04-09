from __main__ import g_logc

class TmpNexpectedException(Exception): pass

#======================================================================================================================
# Cast dtyp
#======================================================================================================================

# key is (dstDtyp, srcDtyp)

CastD = {
    ('str','int'): lambda x: f'chr({x})',
    ('int','str'): lambda x: f'ord({x})',
}    

def castIden(x): return x

class DtypNone:
    @staticmethod
    def dtyp():
        return None

#======================================================================================================================
# Coder
#======================================================================================================================

class Coder:
    def __init__(self):
        self.accV = []
        self.hangX = 1
        
    def acc(self, x):
        self.accV.append(x)

    def cast(self, x, dstDtyp, srcDtyp):
        g_logc.codePyCast(x, dstDtyp, srcDtyp)
        return CastD.get((dstDtyp, srcDtyp), castIden)(x)

    def evalExecText(self):
        #todo? self.accV.append('')
        return '\n'.join(self.accV)

    def execExecText(self, expr):
        if self.hangX:
            self.acc(expr)
        return self.evalExecText()

    def hang(self, x):
        self.hangX = 1
        return x
            
    def nhang(self, x):
        self.hangX = 0
        return x
