from py2neo import Graph, Node, Relationship
import json
from config import graph

graph.run("match (n) detach delete n")
with open("d:\\study\\CodeFolder\\DataStructure_KG\\create_ds2_graph\\relation.csv", encoding='utf-8') as f:
    for line in f.readlines():
        rela_array = line.strip("\n").split(",")
        print(rela_array)
        # 节点1
        graph.run("merge (p:%s {name: '%s'})" % (rela_array[3], rela_array[0]))
        # 节点2
        graph.run("merge (p:%s {name: '%s'})" % (rela_array[4], rela_array[1]))
        # 两节点的关系
        graph.run(
            "MATCH (e:%s), (cc:%s) WHERE e.name='%s' AND cc.name='%s' "
            "CREATE (e)-[r:%s {relation: '%s'}]->(cc) RETURN r"
            % (rela_array[3], rela_array[4], rela_array[0], rela_array[1], rela_array[2], rela_array[2])
        )   
