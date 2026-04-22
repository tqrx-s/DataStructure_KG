# -*- coding: utf-8 -*-
import pyltp
import os
import jieba

LTP_DATA_DIR = 'D:/Program Files (x86)/study/graduation Project/DataStructure_KG-master/KGQA/ltp_data_v3.4.0'  # ltp模型目录的路径
getpath = os.path.abspath(os.path.dirname(__file__))  # 获取本层目录
getpath = ('/').join(getpath.split('\\'))

def cut_words(words):
    # list1 = jieba.lcut(words)
    jieba.load_userdict(getpath + "/my_dict.txt")# 加载自定义词典
    array = jieba.lcut(words)# 对文本进行分词
    # print(array)
    return array


# a = cut_words("数组的分类有哪些？")
# print(a)

# 定义词性标注函数
def words_mark(array):
    # 词性标注模型路径，模型名称为`pos.model`
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    postagger = pyltp.Postagger(pos_model_path)  # 初始化实例
    # postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(array)  # 词性标注
    pos_str = ' '.join(postags)
    pos_array = pos_str.split(" ")  # 将词性标注结果转化为列表
    postagger.release()  # 释放模型
    return pos_array


def get_target_array(words):
    target_pos = ['n', 'v']# 目标词性为名词和动词
    target_array = []
    seg_array = cut_words(words) # 对文本进行分词
    pos_array = words_mark(seg_array)# 对分词结果进行词性标注
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])# 将满足目标词性的词添加到目标词组中
    return target_array


def get_fuzzy_array(words):
    seg_array = cut_words(words) # 对文本进行分词
    return seg_array


# target_array = get_fuzzy_array("快排序")
# print(target_array)
