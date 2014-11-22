#! /usr/bin/python
import sys
sys.path.append('../')
from toolbox.hreaders import token_readers as reader
from toolbox.hmappers import simple_mapper as mapper
 
_map = mapper.Simple_mapper(1,3)
_reader = reader.Token_reader()

for line in sys.stdin:
    words = _reader.read_all(line)
    new_key = map(int,_map.get_key(words).split('/'))[1]
    print '{}\t{}'.format(new_key, _map.get_value(words))