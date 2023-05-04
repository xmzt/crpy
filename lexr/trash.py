[v7]
  160   370  6352 actlib.py
   24   107  1111 cbase.py
  201   595  5701 chtab.py
  190   989  8309 clex.py
   54   100  1456 codepylib.py
  147   330  5162 funlib.py
  176   407  6214 logclib.py
  302   784 10478 machlib.py
  777  1684 24980 nodelib.py
  462   947 13754 objlib.py
  180   488  5763 scanlib.py
   85   232  2253 util.py
 2758  7033 91533 total

#======================================================================================================================
# loglib
#======================================================================================================================

def LogcMeta(name, bases, namespace, **kwds):
    namespace[k] = keyCall something or other

def logcWrap(k):
    def f(self, *args, **kwds):
        return self.keyCall(k, *args, **kwds)
    return f

class LogcContext:
    def __init__(self, logc):
        self.logc = logc

    def __enter__(self):
        self.logc.context = LogcContext(self.logc) # for nested calls
        self.prevDeque = collections.deque()
        self.logc.indInc(self.prevDeque)
        
    def __exit__(self, *args):
        self.logc.indDec(self.prevDeque)

class Logc:
    def __init__(self, up, **kwds):
        self.up = up
        #self.logr
        self.kvD = {k:0 for k in self.KeyDset} 
        self.kvSet(**kwds)
        self.prev = 0
        self.context = LogcContext(self)

    def keyCall(self, k, *args, **kwds):
        v = self.prev = self.kvD[k]
        if v:
            getattr(self, f'{k}__{v}')(*args, **kwds)
        if None is not self.up:
            self.up.keyCall(k, *args, **kwds)
        return self.context
    
    def indInc(self, prevDeque):
        prevDeque.append(self.prev)
        if self.prev:
            self.logr.indInc()
        if None is not self.up:
            self.up.indInc(prevDeque)

    def indDec(self, prevDeque):
        if prevDeque.popleft():
            self.logr.indDec()
        if None is not self.up:
            self.up.indDec(prevDeque)

    def prevDequeGet(self, prevDeque):
        prevDeque.append(self.prev)
        if None is not self.up:
            self.up.prevDequeGet(prevDeque)
    
    def todofunSet(self, k, v):
        f0 = getattr(self, f'{k}__{v}')
        if None is self.up:
            setattr(self, k, f0)
        else:
            def f1(*args, **kwds):
                getattr(self.up, k)(*args, **kwds)
                return f0(*args, **kwds)
            setattr(self, k, f1)
            
    def todokvSet(self, **kwds):
        for k,v in kwds.items():
            if k in self.kvD:
                self.kvD[k] = v
                self.funSet(k, v)
            else:
                setattr(self, k, v)
        return self

class TodoLogcSwapLogrPath:
    def __init__(self, logc, path):
        self.logc = logc
        self.logr0 = logc.logr
        logc.logr = Logr5File(open(path, 'w'))
        
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.logc.logr.file0.close()
        self.logc.logr = self.logr0
    
    

#======================================================================================================================
# Coder
#======================================================================================================================

class Logc:
    def codePyPre__1(self, coder, text, expr):
        with self.logr(f'[codePyPre]'):
            self.logr(f'acc:').inMl(text)
            return self.logr(f'expr: {expr!r}')
            
    def codePyRes__1(self, res):
        return self.logr(f'res: {util.desTyp(res)}')

class Coder:
    def evalGo(self, expr, glos, locs):
        text = self.evalExecText()
        with g_logc.codePyPre(self, text, expr):
            exec(text, glos, locs)
            res = eval(expr, glos, locs)
            g_logc.coderes(res)
            return res

    def execGo(self, expr, glos, locs):
        text = self.execExecText(expr)
        with g_logc.codePyPre(self, text, ''):
            exec(text, glos, locs)



class CoderTmp(CoderNtmp):
    def __init__(self, inComp, glos, locs):
        super().__init__(inComp)
        self.glos = glos
        self.locs = locs
        self.tmpI0 = locs['_tmpI']
        
    def __enter__(self):
        return self

    def __exit__(self, *args):
        for i in range(self.locs['_tmpI'], self.tmpI0, -1):
            try:
                del self.locs[f'_tmp{i}']
            except KeyError:
                pass
        self.locs['_tmpI'] = self.tmpI0

    def evalGo(self, expr):
        return super().evalGo(expr, self.glos, self.locs)
        
    def execGo(self, expr):
        return super().execGo(expr, self.glos, self.locs)

    def tmp(self, val):
        self.locs['_tmpI'] += 1
        self.locs[sym := f"_tmp{self.locs['_tmpI']}"] = val
        return sym

