from py2neo import Graph, Node, Relationship
import json
from config import graph
import sys
sys.path.append("..")



def add_node(e1, e2, rel, c1, c2):
    # message = "添加成功"
    a = [e1, e2, rel, c1, c2]
    num1 = graph.run("MATCH (m:Concept {name:'%s' })return count(m)" % e1).data()[0]['count(m)']
    num2 = graph.run("MATCH (m:Concept {name:'%s' })return count(m)" % e2).data()[0]['count(m)']
    if num1 == 0 and num2 == 0 :
        graph.run("CREATE(n:Concept {name:'%s', cate:'%s'})-[r:%s{relation: '%s'}]->(m:Concept {name:'%s', cate:'%s'})" % (e1, c1, rel, rel, e2, c2))
    if num1 != 0 and num2 == 0:
        graph.run("MATCH(m: Concept {name: '%s', cate:'%s'}) CREATE(m) - [r:%s{relation: '%s'}]->(n:Concept {name:'%s', cate:'%s'})"  % (e1, c1, rel,rel, e2, c2))
    if num1 == 0 and num2 != 0:
        graph.run("MATCH(m: Concept {name: '%s', cate:'%s'}) CREATE(n:Concept {name:'%s', cate:'%s'})-[r:%s{relation: '%s'}]->(m)"  % (e2, c2, e1, c1, rel, rel))
    # num = data
    if num1 != 0 and num2 != 0:
        graph.run("MATCH(m: Concept {name: '%s'}),(n:Concept {name:'%s'}) CREATE (m)-[r:%s{relation: '%s'}]->(n)"  % (e2, e1, rel, rel))
        # message = "此条关系已存在！"
    # print(num1, num2, message)

    # MATCH(m: Concept {name: 'C语言'}) CREATE(m) - [: 包括]->(n:Concept {name:'函数'}) return m
    # graph.run("CREATE(n:Concept {name:'%s', cate:'%s'}) return n") %(e1,e2)
    print(a)
    # return message


add_node('1','2','3','4','5')



