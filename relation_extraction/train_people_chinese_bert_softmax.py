import sys, json
import torch
import os
import numpy as np
import opennre
from opennre import encoder, model, framework
import argparse

# argparse是python用于解析命令行参数和选项的标准模块
parser = argparse.ArgumentParser()  # 创建一个解析对象
parser.add_argument('--mask_entity', action='store_true', help='Mask entity mentions')
# 向该对象中添加关注的命令行参数和选项，每一个add_argument方法对应一个要关注的参数或选项
args = parser.parse_args()  # 最后调用parse_args()方法进行解析，解析成功之后即可使用

# Some basic settings
root_path = '.'
sys.path.append(root_path)  # sys.path.append('需要引用模块的地址')
if not os.path.exists('ckpt'):  # 如果不存在这个目录
    os.mkdir('ckpt')  # 就创建一个
ckpt = 'ckpt/people_chinese_bert_softmax.pth.tar'

# Check data 关系
rel2id = json.load(open(os.path.join(root_path, 'benchmark/people-relation/people-relation_rel2id.json'), encoding='utf-8'))

# Define the sentence encoder
sentence_encoder = opennre.encoder.BERTEncoder(  # bert encoder
    max_length=80, 
    pretrain_path=os.path.join(root_path, 'pretrain/chinese_wwm_pytorch'),
    mask_entity=args.mask_entity
)

# Define the model
model = opennre.model.SoftmaxNN(sentence_encoder, len(rel2id), rel2id)

# Define the whole training framework
framework = opennre.framework.SentenceRE(  # 普通句子级别的关系抽取流程 sentence_re
    train_path=os.path.join(root_path, 'benchmark/people-relation/people-relation_train.txt'),
    val_path=os.path.join(root_path, 'benchmark/people-relation/people-relation_val.txt'),
    test_path=os.path.join(root_path, 'benchmark/people-relation/people-relation_val.txt'),
    model=model,
    ckpt=ckpt,
    batch_size=64, # Modify the batch size w.r.t. your device
    max_epoch=3,
    lr=2e-5,  # learning rate
    opt='adamw'  # Adam + weight decate
)

# Train the model
framework.train_model()

# Test the model
# load_state_dict()函数用于将预训练的参数权重加载到新的模型之中
framework.load_state_dict(torch.load(ckpt)['state_dict'])
result = framework.eval_model(framework.test_loader)

# Print the result
print('Accuracy on test set: {}'.format(result['acc']))
