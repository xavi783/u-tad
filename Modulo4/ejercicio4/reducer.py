#! /usr/bin/python
import sys
sys.path.append('../')
from toolbox.hreaders import token_readers as reader
from toolbox.hreducers import list_reducer as reducer

def reduction(x,y,count):
    count[0]+=1
    return int(x)+int(y)

_reader = reader.Token_reader("\t",1)
_reducer = reducer.List_reducer(reduction) #x: previous reduction result, y: next element

count = [1]
for line in sys.stdin:
    key, value = _reader.read_all(line)
    K,V = _reducer.reduce(key,value,count)
    if K:
        print '{}\t{:.2f}'.format(K,float(V)/count[0])
        count=[1]
print '{}\t{:.2f}'.format(key,float(_reducer.out)/count[0])