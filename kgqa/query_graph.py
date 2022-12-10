# 问答系统查询图数据库模块
import sys
from neo_db.config import graph
sys.path.append('../')


# 使用分词后抽取标注好词性的array进行数据库查询语言构建
def get_kgqa_answer(array):
    data_array = []
    for i in range(1):
        if i == 0:
            name = array[0]
        else:
            name = data_array[-1]['p.Name']
        data = graph.run(
            "match(p)<-[r:%s{relation: '%s'}]-(n:Entity{Name:'%s'}) return  p.Name,n.Name,r.relation" % (
                array[i + 1], array[i + 1], name)
        )
        data = list(data)
        data_array.extend(data)
    return data_array


# 测试用代码
if __name__ == '__main__':
    a1 = ['哈米什·麦克法兰', '职业', '的']
    a2 = ['哈利·波特', '学生', '是']
    a3 = ['乔治·韦斯莱', '从属']
    a4 = ['乔治·韦斯莱', '叔叔', '的']
    res = get_kgqa_answer(a1)
    for i in res:
        print(i[0])
