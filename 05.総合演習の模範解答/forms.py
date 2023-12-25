from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,IntegerField,SelectField
from wtforms.validators import DataRequired,Length,NumberRange


class ProductForm(FlaskForm):
    name = StringField('商品名',validators=[DataRequired()
        ,Length(max=20,message='20文字以内で入力してください')])
    price = IntegerField('価格',validators=[DataRequired(message='価格は必須です')
        ,NumberRange(min=10,max=100000,message='価格が不正')])
    category = SelectField('カテゴリー', coerce=int)
    submit = SubmitField('送信')

class CategoryForm(FlaskForm):
    name = StringField('カテゴリー名',validators=[DataRequired()
        ,Length(max=20,message='20文字以内で入力してください')])
    submit = SubmitField('送信')

class LoginForm(FlaskForm):
    id = IntegerField('ID',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('ログイン')

class SearchForm(FlaskForm):
    name = StringField('商品名')
    submit = SubmitField('絞り込み')
