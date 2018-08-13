#coding=utf-8
from flask import request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from auth import auth
from run import db, app, login_manager, User
from pyrad.client import Client
from pyrad.dictionary import Dictionary
import pyrad.packet
 
class LoginForm(FlaskForm):
    username = StringField('电子邮箱', validators=[InputRequired(), Email(message='请用邮箱'), Length(max=100)])
    password = PasswordField ('密码', validators = [InputRequired(),Length(min=8,max=80)])
    remember = BooleanField ('保持登陆状态')

@auth.route('/login', methods=['GET','POST'])
def login():
    form  = LoginForm()
    if  form.validate_on_submit():
        srv = Client(server="192.168.1.52", secret=b"matrixchina",dict=Dictionary("dictionary.py"))
            
        # create request
        req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name=form.username.data, NAS_Identifier="192.168.1.52")
        req["User-Password"] = req.PwCrypt(form.password.data)
        
        # send request
        reply = srv.SendPacket(req)
        
        if reply.code == pyrad.packet.AccessAccept:
            print("access accepted")
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                login_user(user,remember= form.remember.data)
            else:
                new_user = User(username=form.username.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=form.remember.data)
        else:
            print("access denied")
            flash('用户名或密码错误，请重新登陆')
            return redirect(url_for('auth.login'))
        
        print("Attributes returned by server:")
        for i in reply.keys():
            print("%s: %s" % (i, reply[i]))
            
    return render_template('auth/login.html',form = form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('用户名已存在，请填写新的用户名')
            return redirect(url_for('auth.signup'))
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('电子邮箱已存在，请填写新的电子邮箱')
            return redirect(url_for('auth.signup'))
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('账号创建成功，请登陆')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('asset.invest_list'))
