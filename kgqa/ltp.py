# ltp模型，用于问答系统用户输入问题进行语义分析并提取
import pyltp
import os

# ltp模型目录的路径. 可从该地址下载：http://model.scir.yunfutech.com/model/ltp_data_v3.4.0.zip
LTP_DATA_DIR = os.path.join(os.getcwd(), 'kgqa/ltp_data_v3.4.0')  # 将这里的路径改为自己本地的地址，该地址为下载好的模型文件夹放在kgqa下

def cut_words(words):
    # 分词模型，模型名称为`cws.model`
    segmentor = pyltp.Segmentor(os.path.join(LTP_DATA_DIR, 'cws.model'))  # 初始化实例
    words = segmentor.segment(words)  # 分词
    array_str = "|".join(words)  # 使用竖线分隔
    array = array_str.split("|")  # 分隔后变为array
    segmentor.release()  # 释放模型
    return array


def words_mark(array):
    # 词性标注模型路径，模型名称为`pos.model`
    postagger = pyltp.Postagger(os.path.join(LTP_DATA_DIR, 'pos.model'))  # 初始化实例
    postags = postagger.postag(array)  # 词性标注
    pos_str = ' '.join(postags)  # 使用空格分隔
    pos_array = pos_str.split(" ")  # 分隔后变为array
    postagger.release()  # 释放模型
    return pos_array


def get_target_array(words):
    # 将上述两个模型融合
    target_pos = ['nh', 'n']  # 实体的词性标注集
    target_array = []  # 待返回的结果集
    seg_array = cut_words(words)  # 首先对输入文本进行分词
    print(seg_array)
    pos_array = words_mark(seg_array)  # 进行词性标注
    print(pos_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])  # 在返回结果集中添加分词后的文本
    target_array.append(seg_array[1])  # 在结果集中添加谓语
    return target_array
