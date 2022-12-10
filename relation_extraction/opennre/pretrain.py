from . import encoder
from . import model
from . import framework
import torch
import os
import sys
import json
import numpy as np

default_root_path = os.path.join('D:/pythonwork/harrypotter/relation_extraction', '.')
# os.path.join()路径拼接 保证在不同操作系统中运行代码的时候都可以得到正确的路径拼接

def check_root(root_path=default_root_path):
    if not os.path.exists(root_path):  # 如果该目录不存在
        os.mkdir(root_path)  # 创建单层目录
        os.mkdir(os.path.join(root_path, 'benchmark'))
        os.mkdir(os.path.join(root_path, 'pretrain'))
        os.mkdir(os.path.join(root_path, 'ckpt'))

# 自动下载数据集
def download_wiki80(root_path=default_root_path):
    check_root()  # 执行上一个函数
    if not os.path.exists(os.path.join(root_path, 'benchmark/wiki80')):  # 如果这个目录不存在
        os.mkdir(os.path.join(root_path, 'benchmark/wiki80'))  # 创建这个目录
        os.system('wget -P ' + os.path.join(root_path, 'benchmark/wiki80') + ' http://193.112.16.83:8080/opennre/benchmark/wiki80/wiki80_rel2id.json')
        os.system('wget -P ' + os.path.join(root_path, 'benchmark/wiki80') + ' http://193.112.16.83:8080/opennre/benchmark/wiki80/wiki80_train.txt')
        os.system('wget -P ' + os.path.join(root_path, 'benchmark/wiki80') + ' http://193.112.16.83:8080/opennre/benchmark/wiki80/wiki80_val.txt')
        # system函数可以将字符串转化成命令在服务器上运行
        # wget -P 路径 网址：将网页内容下载到指定路径
def download_nyt10(root_path=default_root_path):
    check_root()
    if not os.path.exists(os.path.join(root_path, 'benchmark/nyt10')):
        os.mkdir(os.path.join(root_path, 'benchmark/nyt10'))
        os.system('wget -P ' + os.path.join(root_path, 'benchmark/nyt10') + ' http://193.112.16.83:8080/opennre/benchmark/nyt10/nyt10_rel2id.json')
        os.system('wget -P ' + os.path.join(root_path, 'benchmark/nyt10') + ' http://193.112.16.83:8080/opennre/benchmark/nyt10/nyt10_train.txt')
        os.system('wget -P ' + os.path.join(root_path, 'benchmark/nyt10') + ' http://193.112.16.83:8080/opennre/benchmark/nyt10/nyt10_test.txt')
        os.system('wget -P ' + os.path.join(root_path, 'benchmark/nyt10') + ' http://193.112.16.83:8080/opennre/benchmark/nyt10/nyt10_val.txt')

def download_glove(root_path=default_root_path):
    check_root()
    if not os.path.exists(os.path.join(root_path, 'pretrain/glove')):
        os.mkdir(os.path.join(root_path, 'pretrain/glove'))
        os.system('wget -P ' + os.path.join(root_path, 'pretrain/glove') +  ' http://193.112.16.83:8080/opennre/pretrain/glove/glove.6B.50d_mat.npy')
        os.system('wget -P ' + os.path.join(root_path, 'pretrain/glove') +  ' http://193.112.16.83:8080/opennre/pretrain/glove/glove.6B.50d_word2id.json')

def download_bert_base_uncased(root_path=default_root_path):
    check_root()
    if not os.path.exists(os.path.join(root_path, 'pretrain/bert-base-uncased')):
        os.mkdir(os.path.join(root_path, 'pretrain/bert-base-uncased'))
        os.system('wget -P ' + os.path.join(root_path, 'pretrain/bert-base-uncased') + ' http://193.112.16.83:8080/opennre/pretrain/bert-base-uncased/config.json')
        os.system('wget -P ' + os.path.join(root_path, 'pretrain/bert-base-uncased') + ' http://193.112.16.83:8080/opennre/pretrain/bert-base-uncased/pytorch_model.bin')
        os.system('wget -P ' + os.path.join(root_path, 'pretrain/bert-base-uncased') + ' http://193.112.16.83:8080/opennre/pretrain/bert-base-uncased/vocab.txt')

def download_pretrain(model_name, root_path=default_root_path):
    ckpt = os.path.join(root_path, 'ckpt/' + model_name + '.pth.tar')  # 模型文件
    if not os.path.exists(ckpt): # 没有就下载
        print("*"*20)
        print("下载ckpt")
        os.system('wget -P ' + os.path.join(root_path, 'ckpt/')  + ' http://193.112.16.83:8080/opennre/ckpt/' + model_name + '.pth.tar')

def get_model(model_name, root_path=default_root_path):
    check_root()
    ckpt = os.path.join(root_path, 'ckpt/' + model_name + '.pth.tar')  # 模型文件
    
    if model_name == 'wiki80_cnn_softmax':
        print("*"*20+"taorui")
        download_pretrain(model_name)
        download_glove()
        download_wiki80()
        # encode模块主要是对文本进行embeding的操作。
        # 词嵌入实际上是一种将各个单词在预定的向量空间中表示为实值向量的一类技术，每个单词被映射成一个向量（初始随机化），并且这个向量可以通过神经网络的方式来学习更新
        wordi2d = json.load(open(os.path.join(root_path, 'pretrain/glove/glove.6B.50d_word2id.json')))  # 从json文件中读取数据
        word2vec = np.load(os.path.join(root_path, 'pretrain/glove/glove.6B.50d_mat.npy'))
        rel2id = json.load(open(os.path.join(root_path, 'benchmark/wiki80/wiki80_rel2id.json')))
        sentence_encoder = encoder.CNNEncoder(token2id=wordi2d,  # dictionary of token->idx mapping
                                                     max_length=40,  # 句子的最大长度，用于位置嵌入
                                                     word_size=50,  # 单词嵌入大小
                                                     position_size=5,  # 位置嵌入大小
                                                     hidden_size=230,
                                                     blank_padding=True,  # padding for CNN
                                                     kernel_size=3,
                                                     padding_size=1,
                                                     word2vec=word2vec,  # pretrained word2vec numpy
                                                     dropout=0.5)
        m = model.SoftmaxNN(sentence_encoder, len(rel2id), rel2id)
        # 在Pytorch中构建好一个模型后，一般需要进行预训练权重中加载
        m.load_state_dict(torch.load(ckpt)['state_dict'])  # load_state_dict()函数用于将预训练的参数权重加载到新的模型之中
        return m
    elif model_name == 'wiki80_bert_softmax':
        download_pretrain(model_name)
        download_bert_base_uncased()
        download_wiki80()
        rel2id = json.load(open(os.path.join(root_path, 'benchmark/wiki80/wiki80_rel2id.json')))
        sentence_encoder = encoder.BERTEncoder(
            max_length=80, pretrain_path=os.path.join(root_path, 'pretrain/bert-base-uncased'))
        m = model.SoftmaxNN(sentence_encoder, len(rel2id), rel2id)
        m.load_state_dict(torch.load(ckpt)['state_dict'])
        return m
    elif model_name == 'test_chinese_bert_softmax':
        download_pretrain(model_name)
        download_bert_base_uncased()
        download_wiki80()
        rel2id = json.load(open(os.path.join(root_path, 'benchmark/test_chinese/test_chinese_rel2id.json')))
        sentence_encoder = encoder.BERTEncoder(
            max_length=80, pretrain_path=os.path.join(root_path, 'pretrain/chinese_wwm_pytorch'))
        m = model.SoftmaxNN(sentence_encoder, len(rel2id), rel2id)
        m.load_state_dict(torch.load(ckpt)['state_dict'])
        return m

    elif model_name == 'people_chinese_bert_softmax':
        download_pretrain(model_name)
        download_bert_base_uncased()
        download_wiki80()
        rel2id = json.load(open(os.path.join(root_path, 'benchmark/people-relation/people-relation_rel2id.json')))  # 关系文件
        sentence_encoder = encoder.BERTEncoder(
            max_length=80, pretrain_path=os.path.join(root_path, 'pretrain/chinese_wwm_pytorch'))
        m = model.SoftmaxNN(sentence_encoder, len(rel2id), rel2id)
        m.load_state_dict(torch.load(ckpt)['state_dict'])
        return m 

    elif model_name == 'people_delunknown_chinese_bert_softmax':
        download_pretrain(model_name)
        download_bert_base_uncased()
        download_wiki80()
        rel2id = json.load(open(os.path.join(root_path, 'benchmark/people-relation-delunknow/people-relation_rel2id.json')))
        sentence_encoder = encoder.BERTEncoder(
            max_length=80, pretrain_path=os.path.join(root_path, 'pretrain/chinese_wwm_pytorch'))
        m = model.SoftmaxNN(sentence_encoder, len(rel2id), rel2id)
        m.load_state_dict(torch.load(ckpt)['state_dict'])
        return m
    
    else:
        raise NotImplementedError
