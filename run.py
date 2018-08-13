#coding=utf-8
import os
from flask import Flask, template_rendered
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            template_folder='templates',  # 指定模板路径，可以是相对路径，也可以是绝对路径。
            static_folder='static',  # 指定静态文件前缀，默认静态文件路径同前缀
            #static_url_path='/opt/auras/static',     #指定静态文件存放路径。
            )

app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


class User(UserMixin, db.Model):
    from run import db
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from invest import invest
app.register_blueprint(invest, url_prefix='/invest')  # 注册asset蓝图，并指定前缀。
from auth import auth
app.register_blueprint(auth, url_prefix='/auth')  # 注册asset蓝图，并指定前缀。

if __name__ == '__main__':
         # 运行flask http程序，host指定监听IP，port指定监听端口，调试时需要开启debug模式。
         app.run(host='0.0.0.0', port=5000)
