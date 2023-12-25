from flask import Flask, request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pg0MMXM2V8BgTvIXk7ikHA'

class BmiForm(FlaskForm):
    height = StringField('身長(cm)',validators=[DataRequired()
        ,Length(min=2,max=3,message='身長が不正な値です')])
    weight = StringField('体重(kg)',validators=[DataRequired()
        ,Length(min=2,max=3,message='体重が不正な値です')])
    submit = SubmitField('BMIを計算する')

@app.route('/',methods=['GET','POST'])
def index():
    bmi = 0
    best_weight = 0
    judg = ""
    form = BmiForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            height = int(form.height.data) / 100
            weight = int(form.weight.data)
            
            bmi = round( weight / (height * height) , 2)
            best_weight = round( height * height * 22 , 2)

            if bmi < 18.5:
                judg = "低体重(痩せ型)"
            elif bmi < 25:
                judg = "普通体重"
            elif bmi < 30:
                judg = "肥満(1度)"
            elif bmi < 35:
                judg = "肥満(2度)"
            elif bmi < 40:
                judg = "肥満(3度)"
            else:
                judg = "肥満(4度)"

    return render_template('bmi.html', form=form, bmi=bmi, best_weight=best_weight, judg=judg)

if __name__ == '__main__':
    app.run(debug=True)
