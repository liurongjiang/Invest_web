#coding=utf-8
import logging
from flask import request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from auth import auth
from run import db,app, login_manager, User

from pyrad.client import Client
from pyrad.dictionary import Dictionary
import pyrad.packet

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s:%(levelname)s:%(asctime)s:%(message)s')
file_handler = logging.FileHandler('logs/auth.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class LoginForm(FlaskForm):
    username = StringField('电子邮箱', validators=[InputRequired(), Email(message='请用邮箱'), Length(max=100)])
    password = PasswordField ('密码', validators = [InputRequired(),Length(min=8,max=80)])
    remember = BooleanField ('保持登陆状态')

@auth.route('/login', methods=['GET','POST'])
def login():
    server = app.config['AUTH_SERVER']
    secret = app.config['AUTH_SECRET']
    nas_id = app.config['NAS_ID']

    form  = LoginForm()
    if  form.validate_on_submit():
        srv = Client(server=server, secret=secret,dict=Dictionary("dictionary.py"))

        #test account
        if ('test' in form.username.data):
            print("access accepted")
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                login_user(user, remember=form.remember.data)
            else:
                new_user = User(username=form.username.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=form.remember.data)
                logger.info('{}:{} created'.format(current_user.id, new_user.username))
            logger.info('{}:{} login'.format(current_user.username, current_user.id))
            return redirect(url_for('asset.invest_list'))

        # create request
        req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name=form.username.data, NAS_Identifier=nas_id)
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
            return redirect(url_for('asset.invest_list'))
        else:
            print("access denied")
            flash('用户名或密码错误，请重新登陆')
            return redirect(url_for('auth.login'))
        
        print("Attributes returned by server:")
        for i in reply.keys():
            print("%s: %s" % (i, reply[i]))
            
    return render_template('auth/login.html',form = form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('asset.invest_list'))
