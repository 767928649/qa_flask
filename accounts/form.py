# -*- coding: utf-8 -*-
# @Time    : 2022/5/20 上午11:10
# @Author  : Ly
import hashlib
from flask import request
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from models import User, UserProfile, UserLoginHistory, db
from utils import constants
from utils.validators import phone_number


class RegisterForm(FlaskForm):
    """
    用户注册
    """
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    },  validators=[DataRequired(message="用户名不能为空!"), phone_number])
    nickname = StringField(label='昵称', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入昵称'
    }, validators=[DataRequired('昵称不能为空!'),
                   Length(min=2, max=20, message='昵称长度在2-20之间')])
    password = PasswordField(label='密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[DataRequired('密码不能为空!'),
                   Length(min=6, max=20, message='密码长度为2-20之间')])
    confirm_pwd = PasswordField(label='确认密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请重复密码'
    }, validators=[DataRequired('确认密码不能为空'),
                   EqualTo('password', message='两次密码输入不一致')])

    def validate_username(self, field):
        """
        检测用户名是否已存在
        由flask框架自动实现的，表单模型类继承了FlaskForm类，表单模型类实例化时，会自动调用这个验证方法，定义的验证方法必须是以 validate_ 开头，validate_字段名
        :param field:
        :return:
        """
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('该用户已存在')
        return field

    def register(self):
        # 自定义用户注册函数
        # 获取表单信息
        username = self.username.data
        password = self.password.data
        nickname = self.nickname.data
        print(username, nickname, password)
        # 添加到 db.session
        try:
            # 将密码加密存储
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, nickname=nickname, password=password)
            db.session.add(user_obj)
            profile = UserProfile(username=username, user=user_obj)
            db.session.add(profile)
            db.session.commit()
            return user_obj
        except Exception as e:
            print(e)
        return None


class LoginForm(FlaskForm):
    """
    用户登录表单
    """
    username = StringField(label='用户名', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入用户名'
    }, validators=[DataRequired(message="用户名不能为空!"), phone_number])
    password = PasswordField(label='密码', render_kw={
        'class': 'form-control input-lg',
        'placeholder': '请输入密码'
    }, validators=[DataRequired('密码不能为空!'),
                   Length(min=6, max=20, message='密码长度为6-20之间')])

    def validate(self):
        """
        验证账号密码是否正确
        :return:
        """
        result = super().validate()
        username = self.username.data
        password = self.password.data
        if result:
            # 验证加密后的密码是否正确
            user = User.query.filter_by(username=username, password=password).first()
            if user is None:
                result = False
                self.username.errors = ['用户名或者是密码错误']
            elif user.status == constants.UserStatus.user_in_active.value:
                result = False
                self.username.errors = ['用户已被禁用,请联系管理员!']
        return result

    def do_login(self):
        # 1. 查找用户
        username = self.username.data
        password = self.password.data
        try:
            user = User.query.filter_by(username=username, password=password).first()
            # 2. 登录用户
            # 把用户 user_id 加入到 session 中
            # session['user_id'] = user.id
            # 然后我们就需要把我们从数据库中查询到的user模型对象当做参数传入login_user中
            # login_user是一个高度封装的函数，但是它的实质依然是把用户的票据写入到cookie中。其中最关键的的信息就是用户 id 号
            # login_user这个插件他要求我们在我们的用户模型内部定义一个函数，这个函数的名字是固定的叫get_id
            # 然后执行回调函数.带有装饰器@login_manager.user_loader的函数,把 user.id 注册到 session 中去
            login_user(user)  # 对于函数login_user(),当你调用他的时候会设置session['user_id'] = user_id；
            # 3. 记录日志
            ip = request.remote_addr
            ua = request.headers.get('user-agent', None)
            obj = UserLoginHistory(username=username, ip=ip, ua=ua, user=user)
            db.session.add(obj)
            db.session.commit()
            return user
        except Exception as e:
            print(e)
        return None
