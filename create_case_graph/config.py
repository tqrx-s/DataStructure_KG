from py2neo import Graph,GraphService

graph = Graph(
    "bolt://localhost:7687",
    # "http://localhost:11008",
    auth=("neo4j","jianhong2008")
    # auth=("DS Graph Database","jianhong2008")
    # username="neo4j",
    # password="jianhong2008"
)  # DataStructureKG
# CA_LIST = {"案例名称": 0, "时间": 1, "地点": 2, "学生行为1": 3, "学生行为2": 4, "老师行为": 5, "知识点": 6}
CA_LIST = {"案例名称": 0, "时间": 1, "地点": 2, "学生行为": 3, "教师行为": 4, "知识点": 5, "建议":6}
