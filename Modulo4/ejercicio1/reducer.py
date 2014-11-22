#! /usr/bin/python
import sys
sys.path.append('../')
from toolbox.hreaders import token_readers as reader
from toolbox.hreducers import list_reducer as reducer

_reader = reader.Token_reader("\t",1)
_reducer = reducer.List_reducer(lambda x,y: int(x)+int(y)) #x: previous reduction result, y: next element

for line in sys.stdin:
    key, value = _reader.read_all(line)
    K,V = _reducer.reduce(key,value)
    if K:
        print '{}\t{}'.format(K,V)
print '{}\t{}'.format(key,_reducer.out)