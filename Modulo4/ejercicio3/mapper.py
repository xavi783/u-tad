#! /usr/bin/python
import sys
sys.path.append('../')
from toolbox.hreaders import token_readers as reader
from toolbox.hmappers import simple_mapper as mapper
 
_map = mapper.Simple_mapper(1,[0,3])
_reader = reader.Token_reader()

for line in sys.stdin:
    words = _reader.read_all(line)
    print '{}\t{}'.format(_map.get_key(words), _map.get_value(words))