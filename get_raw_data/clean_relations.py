import re

"""去特殊字符函数
去掉"("、")"、"["、"]"、数字和"†"，并且将字符串中有"/"或","，取字符串"/"或"，"的前半截
"""


def clean_r(s):
    s = re.sub(r'\(', '', s)
    s = re.sub(r'\)', '', s)
    s = re.sub(r'\[', '', s)
    s = re.sub(r'\]', '', s)
    s = re.sub(r'\d+', '', s)
    s = re.sub(r'†', '', s)
    if '/' in s:
        s = s.split('/')[0]
    if '，' in s:
        s = s.split('，')[0]
    return s


# 按照每行读取文件内的数据，写入relations。
def read_relations(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        data = f.readlines()
    relations = []
    for row in data:
        d = row.strip().split()
        relations.append(d)
    return relations


# 读取文件内容,传入relations.
relations = read_relations('relations.txt')
clean_relations = []

for d in relations:
    if len(d) != 3: continue  # 如果数据不是三元组的内容，就跳过
    if d[-1][0] == '(' and d[-1][-1] == ')': continue  # 如果三元组中最后一项以“(”起始并且以")"结尾的跳过
    if d[-1] == '-': continue  # 如果三元组最后一项以"-"跳过
    d[1] = clean_r(d[1])  # 执行上面定义的去特殊字符函数
    if d[1] == '可能': continue  # 三元组关系为可能的，跳过
    clean_relations.append(d)  # 将不符合上述四条的三元组计入clean_relations，为清洗后数据

# 将清洗后数据写入文档
with open('relations_clean.txt', 'w', encoding='utf-8') as f:
    for r in clean_relations:
        f.write('%s\t%s\t%s\n' % (r[0], r[1], r[2]))
