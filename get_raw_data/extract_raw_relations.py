from bs4 import BeautifulSoup
import requests
import re

root = 'https://harrypotter.fandom.com/zh/wiki/'

"""
初步清洗
clean_string（s）方法
    利用正则表达式，替换字符串，将中括号里的数字去掉。例如abc[15]de,执行后变abcde。
"""


def clean_string(s):
    s = re.sub(r'\[\d*\]', '', s)
    return s


# 该方法通过获取网页中的关系列表（li标签）获取关系信息
def extract_entity(ent):
    url = root + ent  # 网页地址
    response = requests.get(url=url).content  # 爬取数据
    soup = BeautifulSoup(response, 'html.parser')  # 可以获取html的结构及其内容,包含诸多标签及其类名如<html>、<p>、<a>等。
    e1 = ent
    relations = []
    # 找到页面的div块标签，而且class为如下值的。
    for p in soup.find_all('div', attrs={
        'class': 'pi-item pi-header pi-secondary-font pi-item-spacing pi-secondary-background'}):
        # 找到此class的div标签里的p标签，而且p标签内容为'家庭信息'的。
        if p.text == '家庭信息':
            # 该循环为在该p标签下找兄弟标签,找出所有兄弟标签里块标签div标题为家庭成员的(一般是列表形式),把列表里的内容分别放入relations里。
            for np in p.next_siblings:
                if np.find_all('div')[0].text == '家庭成员':
                    for relation in np.find_all('li'):
                        tmp = relation.text.split()
                        if len(tmp) >= 2:
                            r = (clean_string(tmp[1][1:-1]), clean_string(tmp[0]))
                            relations.append(r)
        # 找到此class的div标签里的p标签，而且p标签内容为'关系信息'的。
        elif p.text == '关系信息':
            # 该循环为在该p标签下找兄弟标签,找出所有兄弟标签，并且r为该标签的内容（如哥哥、父亲等）,再把列表里的内容e（一般为实体名，就是人名）初步清洗后分别放入relations里。
            for np in p.next_siblings:
                r = clean_string(np.find_all('div')[0].text)
                for e2 in np.find_all('li'):
                    e = clean_string(e2.text)
                    if len(e.split()) > 1:
                        for ee in e.split():
                            relations.append((r, ee))
                    else:
                        relations.append((r, e))
    relations = [(e1, r[0], r[1]) for r in relations]
    return relations


# 关系去重，set函数可以去重
all_relations = set()

with open('entities.txt', 'r', encoding='utf-8') as f:
    ents = [e.strip() for e in f.readlines()]
    # 将entities文件中每个实体进行关系获取，调用extract_entity函数获取关系，每个人物关系获取后都放入all_relations里。
    for e in ents:
        print('processing', e)
        relations = extract_entity(e)
        for r in relations:
            all_relations.add(r)

# 将all_relations排序后写入relations文件里。
all_relations = sorted(list(all_relations))
with open('relations.txt', 'w', encoding='utf-8') as f:
    for r in all_relations:
        f.write('%s\t%s\t%s\n' % (r[0], r[1], r[2]))
