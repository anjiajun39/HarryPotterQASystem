from py2neo import Graph
graph = Graph(
    "http://localhost:7474",  # 数据库连接地址
    name="neo4j",  # 数据库用户名
    password="123456"  # 数据库密码
)

