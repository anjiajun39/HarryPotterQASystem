from requests_html import HTMLSession

# 初步手动定义类别：(可能不全)
seeds = ['Category:霍格沃茨职工',
         'Category:霍格沃茨学生',
         'Category:第一次凤凰社',
         'Category:魔法部雇员',
         'Category:食死徒',
         'Category:麻瓜']

# 网站地址的截取部分，后面要加不同的类别爬取不同网站
root = 'https://harrypotter.fandom.com/zh/wiki/'
# # url = 'https://harrypotter.fandom.com/zh/wiki/Category:%E9%9C%8D%E6%A0%BC%E6%B2%83%E8%8C%A8%E5%AD%A6%E7%94%9F'
# session = HTMLSession()
# response = session.get(url)
# a_list = response.html.find('a')
# titles = []
# for a in a_list:
#     if a.attrs.get('class', '') == ('category-page__member-link', ):
#         titles.append(a.attrs['title'])
# print(titles)

# for t in titles:
#     if 'Category' in t:

# 创建承装所有实体的列表
all_entities = []

# 创建要识别的当前类别列表和已经识别的类别列表，数据从我们手动初步创建的类别里提取。
current_category = [x for x in seeds]
have_seen_categories = set([x for x in seeds])

"""
#while循环简介：
    #seed为当前类别列表current_category第0个元素，并将current_category第0个元素弹出
    #url为即将爬取的网址,我们把网址分为两段，第一段为前置链接就是root，第二段是后置链接是seed。
    #建立session
    #response为网页返回码，如404就是未找到等。
    #a_list为查找内容的列表
    #第一个for循环是指要将a_list中所有元素的后置链接seed的class为成员链接的筛选出来
仅保留为category-page__member-link类的链接，并且将title记录到cur_ents中，
title就是人物名(实体)。但是此时title中是包括Template(模板)、Category(类、职位)
和人物名(实体)三种。
    #第二个for循环里第一个if是将Template(模板)的直接跳过，第二个if是筛选Category，
其中该if里的if是判断该Category是不是have_seen_categories里的，如果不是，
则将该Category添加到have_seen_categories和current_category并记录下来，
如果是，则跳过。如果既不是Template又不是Category，则就是我们需要的实体，将实体
记录下来放在all_entities里
"""
while len(current_category) >= 1:
    seed = current_category.pop(0)
    print('visiting', seed)
    url = root + seed
    session = HTMLSession()
    response = session.get(url)
    a_list = response.html.find('a')
    cur_ents = []
    for a in a_list:
        if a.attrs.get('class', '') == ('category-page__member-link',):
            cur_ents.append(a.attrs['title'])
    for t in cur_ents:
        if 'Template' in t: continue
        if 'Category' in t:
            if t not in have_seen_categories:
                current_category.append(t)
                have_seen_categories.add(t)

        else:
            all_entities.append(t)

# 将提取出来的实体all_entities去重复,排序。然后写入entities.txt中。
all_entities = sorted(list(set(all_entities)))
with open('entities.txt', 'w', encoding='utf-8') as f:
    for t in all_entities:
        f.write(t.strip() + '\n')
