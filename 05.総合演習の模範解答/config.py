from flask import Flask

app = Flask(__name__)
app.config['DATABASE_URI'] = './test.db'
app.config['SECRET_KEY'] ='pg0MMXM2V8BgTvIXk7ikHA'

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # login_viewのrouteを設定
