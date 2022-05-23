# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 下午4:24
# @Author  : Ly
from flask_login import logout_user
from accounts.form import RegisterForm, LoginForm
from flask import Blueprint, render_template, flash, redirect, url_for, request

# 创建一个 accounts 的蓝图,然后把注册到 app 里面
accounts = Blueprint('accounts', __name__,
                     static_folder='../assets',
                     template_folder='templates'
                     )


@accounts.route('/login', methods=['GET', 'POST'])
def login():
    # 登录页
    form = LoginForm()
    # 取一下上次浏览的 url,没有的话就跳转到首页
    next_url = request.values.get('next', url_for('qa.index'))
    if form.validate_on_submit():
        user_obj = form.do_login()
        if user_obj:
            flash('%s, 欢迎回来!' % user_obj.nickname, 'success')
            return redirect(next_url)
        else:
            flash('登录失败,请稍后再试', 'danger')
    return render_template('login.html', form=form, next_url=next_url)


@accounts.route('/logout')
def logout():
    """
    退出登录
    :return:
    """
    # 自定义退出登录代码
    # session['user_id'] = ''
    # g.current_user = None
    logout_user()
    flash('欢迎下次再来', 'success')
    return redirect(url_for('accounts.login'))


@accounts.route('/register', methods=['GET', 'POST'])
def register():
    # 注册页
    form = RegisterForm()
    if form.validate_on_submit():
        user_obj = form.register()
        if user_obj:
            flash('注册成功,请登录', 'success')
            return redirect(url_for('accounts.login'))
        else:
            flash('注册失败,请稍后再试', 'danger')
    return render_template('register.html', form=form)


@accounts.route('/mine')
def mine():
    # 个人中心
    return render_template('mine.html')
