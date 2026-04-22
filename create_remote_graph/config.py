from py2neo import Graph,GraphService

graph = Graph(
    # "bolt://localhost:7687",
    "neo4j+s://43746963.databases.neo4j.io",
    auth=("neo4j","AeOMZxDI9qi2l_gEfV4f_cPEeivC8_EqwBwSvrk6Ud8")
)  # DataStructureKG

CA_LIST = {"父节点": 0, "二级概念": 1, "三级概念": 2, "四级概念": 3, "五级概念": 4, "六级概念": 5}
