#! /usr/bin/python
import sys
sys.path.append('../')
from toolbox.hreaders import token_readers as reader
from toolbox.hreducers import list_reducer as reducer

SOLO_FACTURA = False

def reduction(x,y):
    v1 = x.split(',')
    v2 = y.split(',')
    r = x if int(v1[1])>=int(v2[1]) else y
    return r

_reader = reader.Token_reader("\t",1)
_reducer = reducer.List_reducer(reduction) #x: previous reduction result, y: next element

if SOLO_FACTURA:
    for line in sys.stdin:
        key, value = _reader.read_all(line)
        K,V = _reducer.reduce(key,value)
        if K:
            print '{}\t{}'.format(V.split(',')[0],V.split(',')[1])
    V = _reducer.out.split(',')
    print '{}\t{}'.format(V[0],V[1])
else:
    for line in sys.stdin:
        key, value = _reader.read_all(line)
        K,V = _reducer.reduce(key,value)
        if K:
            print '{}\t{}'.format(K,V)
    print '{}\t{}'.format(key,V)