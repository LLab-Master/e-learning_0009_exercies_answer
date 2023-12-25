from flask import Flask, request

app = Flask(__name__)

#数字入力の画面
@app.route('/')
def index():
    html = '''
    数字を2つ入力して下さい
    <br><br>
    <form action="select_calc" method="post">
        <input type="text" name="num1" /><br><br>
        <input type="text" name="num2" /><br><br>
        <input type="submit" value="次の画面へ行く" />
    </form>
    '''
    return html

#四則演算子を選択する画面
@app.route('/select_calc',methods=['POST'])
def select_calc():
    if request.method == 'POST':

        html = '''
        四則演算子を選んで下さい
        <br><br>
        <form action="result" method="post">
        '''

        html += request.form['num1']

        #ドロップダウン作成
        html += '''
        <select name="calc_type">
        <option value="0">+</option>
        <option value="1">-</option>
        <option value="2">×</option>
        <option value="3">÷</option>
        </select>
         '''

        html += request.form['num2']
        
        html += '''<br><br><input type="submit" value="計算結果を見る" />'''
        html += '''<input type="hidden" name="num1" value=''' + request.form['num1'] + ">" #hiddenタグでnum1を次の画面へ持っていく
        html += '''<input type="hidden" name="num2" value=''' + request.form['num2'] + ">" 
        html += "</form>"
        html += '''<br><br><a href="/">前の画面に戻る</a><br>'''


        return html

#計算結果を表示する画面
@app.route('/result',methods=['POST'])
def result():
    if request.method == 'POST':
        calc_type = ""
        result = ""
        if request.form['calc_type'] == "0":
            result = int(request.form['num1']) + int(request.form['num2'])
            calc_type = "+"
        elif request.form['calc_type'] == "1":
            result = int(request.form['num1']) - int(request.form['num2'])
            calc_type = "-"
        elif request.form['calc_type'] == "2":
            result = int(request.form['num1']) * int(request.form['num2'])
            calc_type = "×"
        elif request.form['calc_type'] == "3":
            result = int(request.form['num1']) / int(request.form['num2'])
            calc_type = "÷"
        
        html = str(request.form['num1']) + " " + calc_type + " " + str(request.form['num2']) + " = " + str(result)
        html += '''<br><br><a href="/">最初に戻る</a><br>'''

        return html

#開発用にdebugはTrueにしてる開発が終わったら消すこと
if __name__ == '__main__':
    app.run(debug=True)
