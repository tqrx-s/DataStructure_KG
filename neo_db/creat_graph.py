from config import graph
import sys
sys.path.append("..")

graph.run("match (n) detach delete n")
with open("./raw_data/relation.csv", encoding='utf-8') as f:
    for line in f.readlines():
        rela_array = line.strip("\n").split(",")
        print(rela_array)
        # 节点1
        graph.run("merge (p:Concept {cate:'%s', name: '%s'})" % (rela_array[3], rela_array[0]))
        # 节点2
        graph.run("merge (p: Concept{cate:'%s',name: '%s'})" % (rela_array[4], rela_array[1]))
        # 两节点的关系
        graph.run(
            "MATCH(e: Concept), (cc: Concept) WHERE e.name='%s' AND cc.name='%s' CREATE(e)-"
            "[r:%s{relation: '%s'}]->(cc) RETURN r" % (rela_array[0], rela_array[1], rela_array[2], rela_array[2])
        )

# 添加属性
name_lst = []
with open('./KGQA/my_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        name_lst.append(line.strip('\n'))
with open('./spider/json/data.json', encoding='utf-8')as f:
    data = json.load(f)
    for name in name_lst:
        for i in data[name]:
            print(name, i, data[name][i])
            j = "".join(i.split())
            graph.run('match (n:Concept{name:"%s"}) set n.%s="%s"' % (name, j, data[name][i]))
