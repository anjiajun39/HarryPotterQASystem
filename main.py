from flask import Flask, request, render_template, redirect
from qa_app import get_kgqa_answer, get_target_array

app = Flask(__name__)


# 链接至查询页面
@app.route("/")
def index():
    res = ''
    return render_template("index.html", res = res)


# 接收搜索内容，返回查询结果
@app.route("/search", methods=["POST"])
def search():
    try:
        question = request.form["question"]
        array = get_target_array(question)
        answer = get_kgqa_answer(array)
        res = ''
        for i in answer:
            res += (i[0])
            res += ', '
        question.strip()
        question = '[' + question + ']'
        data = {'ques': question, 'ans': res}
        return render_template("index.html", res = data)
    except Exception as e:  # 若查询无效，返回主界面,将错误打印在terminal中
        print("---------------------")
        print(e)
        return redirect("/")



