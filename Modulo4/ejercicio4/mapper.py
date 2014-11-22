#! /usr/bin/python
import sys
sys.path.append('../')
from toolbox.hreaders import token_readers as reader
from toolbox.hmappers import simple_mapper as mapper

_map = mapper.Simple_mapper(2,3)
_reader = reader.Token_reader()

with open('../clientes.txt') as fd:
    clientes = dict([v.split(',') for v in map(str.strip, fd.readlines())])

for line in sys.stdin:
    words = _reader.read_all(line)
    edad = clientes[words[2]]
    print '{}\t{}'.format(edad, _map.get_value(words))