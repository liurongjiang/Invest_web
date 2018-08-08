#coding=utf-8
from flask import request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from auth import auth
from run import db, app, login_manager, User
# from pyrad.client import Client
# from pyrad.dictionary import Dictionary
# import pyrad.packet
#
# srv = Client(server="localhost", secret=b"Kah3choteereethiejeimaeziecumi",
#              dict=Dictionary("dictionary"))
#
# # create request
# req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest,
#                            User_Name="wichert", NAS_Identifier="localhost")
# req["User-Password"] = req.PwCrypt("password")
#
# # send request
# reply = srv.SendPacket(req)
#
# if reply.code == pyrad.packet.AccessAccept:
#     print("access accepted")
# else:
#     print("access denied")
#
# print("Attributes returned by server:")
# 
# for i in reply.keys():
#     print("%s: %s" % (i, reply[i]))
class LoginForm(FlaskForm):
    username = StringField('用户名', validators= [InputRequired(),Length(min=4,max=100)])
    password = PasswordField ('密码', validators = [InputRequired(),Length(min=8,max=80)])
    remember = BooleanField ('保持登陆状态')

class RegisterForm(FlaskForm):
    email = StringField('电子邮箱',validators=[InputRequired(),Email(message='请用邮箱'),Length(max=100)])
    username = StringField('用户名', validators= [InputRequired(),Length(min=4,max=100)])
    password = PasswordField('密码', validators = [InputRequired(),EqualTo('confirm', message='确认密码不一致！')])
    confirm = PasswordField('确认密码')

@auth.route('/login', methods=['GET','POST'])
def login():
    form  = LoginForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(username= form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user,remember= form.remember.data)
                return redirect(url_for('asset.invest_list'))
            flash('用户名或密码错误，请重新登陆')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html',form = form)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = RegisterForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(username= form.username.data).first()
        if user:
            flash('用户名已存在，请填写新的用户名')
            return redirect(url_for('auth.signup'))
        user = User.query.filter_by(email= form.email.data).first()
        if user:
            flash('电子邮箱已存在，请填写新的电子邮箱')
            return redirect(url_for('auth.signup'))
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email =form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('账号创建成功，请登陆')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('asset.invest_list'))
