#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re  # re 模块使 Python 语言拥有全部的正则表达式功能。
import sys, json  # 导入sys，json 库
import torch  # 导入pytorch
import os  # 在python下写程序，需要对文件以及文件夹或者其他的进行一系列的操作。os便是对文件或文件夹操作的一个工具。
import numpy as np  # 导入数值计算扩展numpy，起别名为np
import opennre  # 导入OpenNRE关系提取
from opennre import encoder, model, framework  # OpenNRE的3个结构
import argparse  # 导入内置的一个用于命令项选项与参数解析的模块argparse
import pandas as pd  # 导入基于NumPy的数据分析工具pandas，起别名为pd
import itertools  # 导入itertools模块

# In[2]:


# 导入关系抽取模型

parser = argparse.ArgumentParser()
# 创建解析器：ArgumentParser对象。命名为paeser
parser.add_argument('--mask_entity', action='store_true', help='Mask entity mentions')
# 添加参数：通过调用 add_argument() 方法完成的。
# 选项字符串的列表：'--mask_entity'
# 当参数在命令行中出现时使用的动作基本类型：'store_true'
# help命令时的说明：'Mask entity mentions'
args = parser.parse_known_args()[0]
# parse_known_args()：当仅获取到基本设置时，如果运行命令中传入了之后才会获取到的其他配置，不会报错；而是将多出来的部分保存起来，留到后面使用


root_path = '.'
sys.path.append(root_path)
# sys.path 是一个列表 list ,它里面包含了已经添加到系统的环境变量路径。
# 通过列表list的append()方法添加自己的引用模块搜索目录；
if not os.path.exists('ckpt'):  # 判断括号里的文件是否存在，括号内的是文件ckpt。
    os.mkdir('ckpt')  # 如果训练后的模型不存在，则以数字权限模式创建目录
ckpt = 'ckpt/people_chinese_bert_softmax.pth.tar'  # 训练后生成的文件路径命名ckpt

rel2id = json.load(
    open(os.path.join(root_path, 'benchmark/people-relation/people-relation_rel2id.json'), encoding='utf-8'))
# 将people-relation_rel2id.json的数据赋值给rel2id
sentence_encoder = opennre.encoder.BERTEncoder(
    max_length=80,
    pretrain_path=os.path.join(root_path, 'pretrain/chinese_wwm_pytorch'),
    mask_entity=args.mask_entity
)

model = opennre.model.SoftmaxNN(sentence_encoder, len(rel2id), rel2id)  # 关系抽取模型
model.load_state_dict(torch.load(ckpt)['state_dict'])  # 加载参数权重

# In[4]:


with open("Harry_Potter.txt", "r", encoding="utf-8") as f:  # 哈利波特全文
    total_lines = [line.strip() for line in f.readlines()]
# 列表推导式，移除txt文件每一行头尾的空格或换行符。将处理后的每一行存储到列表total_lines中。
total_lines = [line for line in total_lines if line != '']
# 将非空的每一行存储到列表total_lines中。

# In[5]:


# 分句
cutLineFlag = ["？", "！", "。", "!"]
# 将"？", "！", "。", "!"作为分句的标志
sentenceList = []
# 处理后的句子列表
for words in total_lines:  # 对处理后的每行进行遍历
    oneSentence = ""  # 赋值
    for word in words:  # 对处理后的每行中的词进行遍历
        if word not in cutLineFlag:  # 判断词中是否含cutlineFlag的五种符号
            oneSentence = oneSentence + word  # 将oneSentence赋值为新增word后的不完全句子
        else:
            oneSentence = oneSentence + word
            if oneSentence.__len__() > 4:  # 如果oneSentence中的元素大于4
                sentenceList.append(oneSentence.strip())  # 去除头尾的空格或换行符，添加到处理后的句子列表
            oneSentence = ""  # 重新赋值

# In[6]:


sentenceList[1997]

# In[7]:


# 获取所有的实体

csv = pd.read_csv("data/harryid.csv", header=0)  # 读取CSV文件到DataFrame,设定header=0替换掉原来存在列名，放入元组csv中
origin_id = list(csv.iloc[:, 1])  # 取所有行索引，列索引为1的数据放入未处理的实体列表中。

total_id = []  # 处理后的实体列表
for id in origin_id:  # 对未处理的实体列表数据进行遍历
    total_id.append(id)  # 将每个全名添加到处理后的实体列表
    for sub_id in id.split('.'):  # 用split对每个全名取本人名（最后的名）
        total_id.append(sub_id)  # 将本人名添加到处理后的实体列表

total_id = list(set(total_id))  # 通过set函数处理为为一个无序不重复的列表
total_id.remove('')  # 移除空格
print("共有实体：", len(total_id))  # 显示共有多少实体

# In[8]:


new_data = []  # 新的数据关系列表
for sentence in sentenceList:  # 对处理好的句子列表进行遍历
    id_loc = []  # 匹配到的实体位置列表
    id_list = []  # 匹配到的实体列表
    for id in total_id:  # 对处理好的实体列表进行遍历
        if id in sentence:  # 实体是否在该句子中
            loc = [(item.start(), item.end() - 1) for item in re.finditer(id, sentence)]
            # 将实体与句子进行匹配，返回查询到实体在句子中所在位置的起始和结束位置，并放入列表loc中
            id_list.append(id)  # 将能匹配到的实体放入该表中
            id_loc.append(loc[0])  # 将匹配到的实体在句子中的位置放入该表中
            # print(id_loc)

    if len(id_loc) >= 2:  # 当匹配到的位置数据大于等于二时
        permute = list(itertools.combinations(range(len(id_list)), 2))
        # 创建一个长度为能匹配到的实体数量的整数列表，并实现两个整数间的两两组合，并放入表permute中
        # print(len(permute))
        for idx in permute:
            if id_list[idx[0]] not in id_list[idx[1]] and id_list[idx[1]] not in id_list[idx[0]]:
                new_data.append({'text': sentence, 'h': {'pos': id_loc[idx[0]]}, 't': {'pos': id_loc[idx[1]]}})
            # 如果两个实体不重复，则新增这两个实体关系数据项，放入列表new_data中

# In[9]:


print("共构造数据集:", len(new_data))

# In[10]:


new_data[0]

# In[11]:


from tqdm import tqdm

relation_list = []
for data in tqdm(new_data):
    text = data['text']
    t_pos = data['t']['pos']
    h_pos = data['h']['pos']
    rela = model.infer(data)  # 调用模型抽取关系
    # 调用模型的infer函数，传递(1)一个段落，(2)第一个实体位置，以及(3)第二个实体位置。该函数返回实体对的预测关系，使用段落作为上下文。
    relation_list.append([text[t_pos[0]:t_pos[1] + 1], text[h_pos[0]:h_pos[1] + 1], rela])

# In[45]:


relation_df = pd.DataFrame(relation_list)
relation_df.to_csv("data/relation_raw.csv", header=False, index=False)

# In[89]:


# 获取已有的关系
existed_relation = pd.read_csv("data/harryRel.csv", header=0)
sub_obj_list = list(zip(existed_relation.iloc[:, 1], existed_relation.iloc[:, 2]))  # 2、3列对应放到一个list里

from collections import Counter

id2count = dict(Counter(list(existed_relation.iloc[:, 1]) + list(existed_relation.iloc[:, 2])))

# In[90]:


obj_list = {}  # [{(sub_obj, obj): {'rela':(rela1, rela2, ...), 'prob':(..), 'sub':(...), 'obj':(...)}}]

for item in relation_list:  # 之前抽取出来的关系
    cand_sub = []
    cand_obj = []
    if item[2][0] != 'unknown' and item[2][1] > 0.95:
        if (item[0], item[1]) not in obj_list.keys():
            obj_list[(item[0], item[1])] = {'relation': [item[2][0]], 'prob': [item[2][1]]}
        else:
            if item[2][0] not in obj_list[(item[0], item[1])]['relation']:  # 合并重复的实体对，以及其所有的候选关系
                obj_list[(item[0], item[1])]['relation'].append(item[2][0])
                obj_list[(item[0], item[1])]['prob'].append(item[2][1])

        for id in origin_id:
            if item[0] in id:
                cand_sub.append(id)
            if item[1] in id:
                cand_obj.append(id)
            obj_list[(item[0], item[1])]['sub'] = cand_sub  # 所有的候选实体
            obj_list[(item[0], item[1])]['obj'] = cand_obj

# In[91]:


new_relation_list = []
for key, value in obj_list.items():
    if len(value['sub']) > 1:  # 如果候选实体中只有一个实体，则直接替代
        sub_count = [id2count[i] for i in value['sub']]
        subobj = value['sub'][np.argmax(sub_count)]
    else:
        subobj = value['sub'][0]

    if len(value['obj']) > 1:  # 若候选实体中有多个实体，则选出现频率最高的那个替代
        obj_count = [id2count[i] for i in value['obj']]
        obj = value['obj'][np.argmax(obj_count)]
    else:
        obj = value['obj'][0]

    if (subobj, obj) not in sub_obj_list and subobj != obj:
        rela = value['relation'][np.argmax(value['prob'])]
        new_relation_list.append([subobj, obj, rela, value['sub'], value['obj']])

# In[18]:


relation_df = pd.DataFrame(new_relation_list)
relation_df.to_csv("data/relation_raw.csv", header=False, index=False)

# In[19]:


# 已经清洗过的数据
# 推理一些空白关系
clean_relation_list = pd.read_csv("data/relation_clean.csv", header=0)
sub_list = list(clean_relation_list.iloc[:, 0])
obj_list = list(clean_relation_list.iloc[:, 1])
rela_list = list(clean_relation_list.iloc[:, 2])
clean_relation_list = list(
    zip(clean_relation_list.iloc[:, 0], clean_relation_list.iloc[:, 1], clean_relation_list.iloc[:, 2]))

# In[21]:


infer_relation = []
for i in range(len(rela_list)):
    if rela_list[i] == '师生':
        infer_relation.append([obj_list[i], sub_list[i], '学生'])

for rela in infer_relation:
    if (rela[0], rela[1]) not in list(zip(sub_list, obj_list)):
        clean_relation_list.append(rela)

# In[ ]:


relation_df = pd.DataFrame(clean_relation_list)
relation_df.to_csv("data/relation_infered.csv", header=False, index=False)
