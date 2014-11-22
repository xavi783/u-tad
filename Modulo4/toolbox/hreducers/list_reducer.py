
class List_reducer():

    def __init__(self,fun):
        self.key = None
        self.out = None
        self.fun = fun

    def reduce(self,key,value,*args,**kwargs):
        # base: no hay key
        # caso 1: self.key!=key
        # caso 2: self.key==key
        if not self.key:
            r = None, self.out
            self.key = key
            self.out = value
        elif not self.key == key:
            r = self.key, self.out
            self.key = key
            self.out = value
        else:
            r = None, self.out
            self.key = key
            self.out = self.fun(self.out, value, *args, **kwargs)
        return r