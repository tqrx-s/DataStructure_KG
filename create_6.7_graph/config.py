from py2neo import Graph,GraphService

graph = Graph(
    "bolt://localhost:7687",
    # "http://localhost:11008",
    auth=("neo4j","jianhong2008")
    # auth=("DS Graph Database","jianhong2008")
    # username="neo4j",
    # password="jianhong2008"
)  # DataStructureKG
# CA_LIST = {"一级概念": 0, "二级概念": 1, "三级概念": 2, "四级概念": 3, "五级概念": 4, "六级概念": 5, "函数": 6}
CA_LIST = {"完全不熟悉": 1, "有点不熟悉": 2, "大致了解": 3, "比较熟悉": 4, "非常熟悉": 5}