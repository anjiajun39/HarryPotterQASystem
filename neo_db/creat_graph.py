import sys
sys.path.append('../')
from py2neo import Graph, Node, Relationship, NodeMatcher
from neo_db.config import *


with open("relations_final.csv") as f:  # 打开将要导入数据库的csv文件
    for line in f.readlines():          # 逐行读取
        rela_array = line.strip("\n").split(",")  # 将回车去除后，以逗号为分界分隔文本为array
        print(rela_array)  # 将文本打印在终端中显示
        rela_array = [rela_array[0], rela_array[-1], rela_array[1]]  # 变更array顺序
        graph.run("MERGE(p: Entity{Name: '%s'})" % (rela_array[0]))  # 若没有该实体，创建
        graph.run("MERGE(p: Entity{Name: '%s'})" % (rela_array[2]))  # 若没有该实体，创建
        graph.run(
            "MATCH(e: Entity), (cc: Entity) \
            WHERE e.Name='%s' AND cc.Name='%s'\
            CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
            RETURN r" % (rela_array[0], rela_array[2], rela_array[1], rela_array[1])
        )  # 将两个实体的节点建立关系
