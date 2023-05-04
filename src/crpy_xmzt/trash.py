#------------------------------------------------------------------------------------------------------------------------
# Scope
#------------------------------------------------------------------------------------------------------------------------

class Scope:
    def __init__(self, iden, glo, *upV):
        self.iden = iden
        self.glo = glo
        self.upV = upV
        self.roV = self.roVFromUpV(self.upV)
        self.idenStiD = {}
        self.primTypD = {}
        self.enumTypD = {}
        self.structTypD = {}
        self.unionTypD = {}

    def roAdd(self, *upV):
        print(f'ZYX Scope.roAdd {self.iden}: {" ".join([sco.iden for sco in upV])}')
        self.upV += upV
        self.roV = self.roVFromUpV(self.upV)
        print(f'    roV={" ".join([sco.iden for sco in self.roV])}')
        
    def roVFromUpV(self, upV):
        # calculate resolution order from upV. should be similar algorithm to python 2.3+ MRO.
        # https://www.python.org/download/releases/2.3/mro/
        roV = [ self ]
        htV = [(tail.pop(), tail) for tail in [list(reversed(sco.roV)) for sco in reversed(upV)]]
        while htV:
            for h0,t0 in htV:
                for h1,t1 in htV:
                    if t1 is not t0 and h0 in t1:
                        break
                else:
                    # head not in any other tail. add to roV and calculate new htV.
                    roV.append(h0)
                    newHtV = []
                    for h1,t1 in htV:
                        if h1 != h0:
                            newHtV.append((h1, t1))
                        elif t1:
                            newHtV.append((t1.pop(), t1))
                    htV = newHtV
                    break
            else:
                raise ScopeResolutionOrderException()
        return roV
        
    def dn(self, iden):
        return Scope(iden, self.glo, self)

#------------------------------------------------------------------------------------------------------------------------
# Mtyp
#------------------------------------------------------------------------------------------------------------------------
    
class Mtyp:
    #Nick = None

    def __init__(self, stiV):
        self.stiV = stiV
        
    def dump(self, logr, pre):
        with logr(f'{pre}{self.__class__.__name__} nick={self.Nick} stiV.n={len(self.stiV)}'):
            with logr(f'stiV'):
                for i,sti in enumerate(self.stiV):
                    sti.dump(logr, f'[{i}] ')
                
    def pyObjCode(self, fieldF): raise Exception()
    def pyFmt(self, fieldF): raise Exception()

class UnknownMtyp(Mtyp):
    Nick = 'unknown'
    
    def pyObjCode(self, fieldF): return f'PyUnicode_FromString("<UNIMPLEMENTED:{self.stiV[0].iden}>")'
    def pyFmt(self, fieldF): return f'{{{fieldF(self.stiV[0])}}}'

class Symtab:
    #todo del self.scope0 = self.scope = Scope(self, None)
        #todo del self.mtypTrie = { None:None }

    #def scopeNew0(self):
    #    return { None:self.scope0 }

    #def scopeSet(self, scope):
    #    self.scope = scope;
    #    return self.scope
        
    #def scopeSetNew(self, scopeUp):
    #    self.scope = { None:scopeUp }
    #    return self.scope
        
    #def scopeSetNew0(self):
    #    self.scope = { None:self.scope0 }
    #    return self.scope
    
    #def scopePop(self):
    #    x = self.scope
    #    self.scope = self.scope[None]
    #    return x

    #def scopePush(self):
    #    self.scope = { None:self.scope }
    #    return self.scope

    #--------------------------------------------------------------------------------------------------------------------
    # mtyp

    def mtypTriePutTypV(self, typV, mtypClas):
        b0 = self.mtypTrie
        for typ in typV:
            typId = id(typ)
            if None is (b1 := b0.get(typId)):
                b1 = b0[typId] = { None:None }
            b0 = b1
        b0[None] = mtypClas

    def mtypVFromStiV(self, mtypV, stiVxs, keyFromSti):
        iE = len(stiV)
        i = 0
        b0 = self.mtypTrie
        runClas = UnknownMtyp
        runA = i
        runE = i + 1
        while True:
            if i < iE and None is not (b1 := b0.get(keyFromSti(stiV[i]))):
                b0 = b1
                i += 1
                if None is not (clas := b0[None]):
                    runClas = clas
                    runE = i
            elif runA < iE:
                mtypV.append(runClas(stiV[runA:runE]))
                i = runE
                b0 = self.mtypTrie
                runClas = UnknownMtyp
                runA = i
                runE = i + 1
            else:
                break
        return mtypV
