from kgqa.query_graph import *
from kgqa.ltp import *

# 问答系统示例文本
examples = [
    '乔治·韦斯莱的叔叔是谁？',
    '哈利·波特的侄女是谁？',
    '乔治·韦斯莱从属于哪里？',
    '哈米什·麦克法兰的职业是？',
]
print('欢迎使用哈利·波特人物关系问答系统')
print('This is an example:')
q = examples[0]
print('Q:%s'%(q))
array = get_target_array(q)
res = get_kgqa_answer(array)
print('A:')
for i in res:
    print(i[0])
print()


# 问答系统入口
if __name__ == "__main__":
    print('请输入您的问题，输入quit可退出')
    while True:
        print("===" * 36)
        q = input('Q:')
        if q == 'quit':
            sys.exit()
        array = get_target_array(q)
        res = get_kgqa_answer(array)
        print('A:')
        for i in res:
            print(i[0])
