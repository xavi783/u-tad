# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 11:02:00 2015

@author: x
"""
import sys
from neo4jrestclient.client import GraphDatabase

def shortest_path(origin,destiny):
    db = GraphDatabase("http://localhost:7474/db/data/")
    q = lambda origin, destiny: """MATCH (from), (to) , path = (from)-[:DOMAIN_LINK*]->(to)
        WHERE from.prop_node_id='%s' AND to.prop_node_id='%s'
        RETURN path AS shortestPath,
        reduce(distance = 0, r in relationships(path) | distance+r.STFIPS1) AS totalDistance,
        nodes(path)
        ORDER BY totalDistance ASC
        LIMIT 1"""%(origin,destiny)
    path = db.query(q(origin,destiny))[0]
    if path==[]:
        print "There is no path"
        return path
    names = [x['data']['prop_node_id'] for x in path[2]]
    print 'Cheaper path: '+' - '.join(names)
    return path
    
if __name__=="__main__":
    path = shortest_path(*sys.argv[1:])