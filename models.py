# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 下午3:55
# @Author  : Ly
from flask import Flask

from utils import constants
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

"""
第一种办法
"""
# user = 'root'
# password = 'root'
# database = 'flask_qa'
# uri = 'mysql+pymysql://%s:%s@localhost:3306/%s' % (user, password, database)
# app.config['SQLALCHEMY_DATABASE_URI'] = uri
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# orm = SQLAlchemy(app)

db = SQLAlchemy()


class User(db.Model):
    """
    `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `nickname` varchar(64) DEFAULT NULL,
  `password` varchar(256) NOT NULL,
  `avatar` varchar(256) DEFAULT NULL,
  `status` smallint(6) DEFAULT NULL COMMENT '用户状态',
  `is_super` smallint(6) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
    """
    __tablename__ = 'accounts_user'
    # 用户 id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户名称不为空.且不能重复
    username = db.Column(db.String(64), nullable=False, unique=True)
    # 用户昵称
    nickname = db.Column(db.String(64))
    # 密码不能为空且加密
    password = db.Column(db.String(256), nullable=False)
    # 头像
    avatar = db.Column(db.String(256))
    # 用户状态是否可以登录系统
    status = db.Column(db.Integer, default=constants.UserStatus.user_active.value, comment='用户状态')
    # 账号权限, 1 2 3 普通账号,可以对所有内容进行管理
    is_super = db.Column(db.Integer, default=constants.UserRole.common.value)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 更新时间
    updated_at = db.Column(db.DateTime, default=datetime.now)

    # user = orm.relationship('UserProfile')

    def __str__(self):
        return self.nickname

    @property
    def is_authenticated(self):
        """
        登录用户
        :return:
        """
        return True

    @property
    def is_active(self):
        # 有效的用户才能登录系统
        return self.status == constants.UserStatus.user_active.value

    @property
    def is_anonymous(self):
        """未登录用户"""
        return False

    def get_id(self):
        # 在这个函数内部我们需要返回可以表示我们用户身份这样的一个字段,id
        return '%s' % self.id


class UserProfile(db.Model):
    """用户的详细信息
    `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `real_name` varchar(64) DEFAULT NULL,
  `maxim` varchar(128) DEFAULT NULL,
  `sex` varchar(16) DEFAULT NULL,
  `address` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,"""
    __tablename__ = 'accounts_user_profile'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 用户名，用于登录
    username = db.Column(db.String(64), unique=True, nullable=False)
    # 用户真实姓名
    real_name = db.Column(db.String(64))
    # 用户的格言
    maxim = db.Column(db.String(128))
    # 性别
    sex = db.Column(db.String(16))
    # 地址
    address = db.Column(db.String(256))
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime,
                           default=datetime.now, onupdate=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 建立用户的一对一关系属性user.profile  profile.user
    user = db.relationship('User', backref=db.backref('profile', uselist=False))


class UserLoginHistory(db.Model):
    """用户登录历史"""
    __tablename__ = 'accounts_login_history'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 用户名，用于登录
    username = db.Column(db.String(64), nullable=False)
    # 账号平台
    login_type = db.Column(db.String(32))
    # IP地址
    ip = db.Column(db.String(32))
    # user-agent
    ua = db.Column(db.String(128))
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 建立与用户的一对多属性,user.history_list
    user = db.relationship('User', backref=db.backref('history_list', lazy='dynamic'))


class Question(db.Model):
    """问题"""
    __tablename__ = 'qa_question'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 问题标题
    title = db.Column(db.String(128), nullable=False)
    # 问题描述
    desc = db.Column(db.String(256))
    # 问题图片
    img = db.Column(db.String(256))
    # 问题详情
    content = db.Column(db.Text, nullable=False)
    # 浏览人数
    view_count = db.Column(db.Integer, default=0)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 排序
    reorder = db.Column(db.Integer, default=0)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 建立与用户的一对多属性,user.question_list
    user = db.relationship('User', backref=db.backref('question_list', lazy='dynamic'))

    @property
    def get_img_url(self):
        return 'medias/' + self.img if self.img else ''

    @property
    def comment_count(self):
        """
        评论数量
        :return:
        """
        return self.answer_list.filter_by(is_valid=True).count()

    @property
    def follow_count(self):
        """
        关注者数量
        :return:
        """
        return self.question_follow_list.filter_by(is_valid=True).count()

    @property
    def answer_count(self):
        """回答数量"""
        return self.answer_list.filter_by(is_valid=True).count()

    @property
    def tags(self):
        """文章标签"""
        return self.tag_list.filter_by(is_valid=True)

    @property
    def love_count(self):
        """点赞的数量"""
        return self.question_follow_list.count()


class QuestionTags(db.Model):
    """ 问题下的标签 """
    __tablename__ = 'qa_question_tags'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 标签名称
    tag_name = db.Column(db.String(16), nullable=False)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('tag_list', lazy='dynamic'))


class Answer(db.Model):
    """  问题的回答 """
    __tablename__ = 'qa_answer'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 回答的内容详情
    content = db.Column(db.Text, nullable=False)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    # 关联的表,也是 Question对象下qa_question标可以查询到 Answer qa_answer表中数据
    question = db.relationship('Question', backref=db.backref('answer_list', lazy='dynamic'))

    @property
    def love_count(self):
        """
        点赞数量
        :return:
        """
        return self.question_love_list.count()

    def comment_list(self, reply_id=None):
        """有效的评论列表"""
        return self.answer_comment_list.filter_by(is_valid=True, reply_id=reply_id)

    @property
    def comment_count(self):
        """
        评论的数量
        :return:
        """
        return self.answer_comment_list.filter_by(is_valid=True).count()


class AnswerComment(db.Model):
    """ 回答的评论 """
    __tablename__ = 'qa_answer_comment'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 评论内容
    content = db.Column(db.String(512), nullable=False)
    # 赞同人数
    love_count = db.Column(db.Integer, default=0)
    # 评论是否公开
    is_public = db.Column(db.Boolean, default=True)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 最后修改的时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 回复ID
    reply_id = db.Column(db.Integer, db.ForeignKey('qa_answer_comment.id'), nullable=True)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联答案
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_comment_list', lazy='dynamic'))
    # 建立与答案的一对多属性
    answer = db.relationship('Answer', backref=db.backref('answer_comment_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_comment_list', lazy='dynamic'))


class AnswerLove(db.Model):
    """ 回答点赞 """
    __tablename__ = 'qa_answer_love'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联答案
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_love_list', lazy='dynamic'))
    # 建立与答案的一对多属性
    answer = db.relationship('Answer', backref=db.backref('answer_love_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_love_list', lazy='dynamic'))


class AnswerCollect(db.Model):
    """ 收藏的回答 """
    __tablename__ = 'qa_answer_collect'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 逻辑删除
    is_valid = db.Column(db.Boolean, default=True)
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 关联答案
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))

    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_collect_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_collect_list', lazy='dynamic'))
    # 建立与答案的一对多属性
    answer = db.relationship('Answer', backref=db.backref('answer_collect_list', lazy='dynamic'))


class QuestionFollow(db.Model):
    """ 关注的问题 """
    __tablename__ = 'qa_question_follow'
    id = db.Column(db.Integer, primary_key=True)  # 主键
    created_at = db.Column(db.DateTime)
    is_valid = db.Column(db.Boolean, default=True, comment='逻辑删除')
    # 关联用户
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))

    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('question_follow_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_follow_list', lazy='dynamic'))


# 反向获取,根据表关系进行获取
# question = Question().answer_list
# print(question)
#
# user = User().history_list
# print(user)
#
# test = User().question_follow_list
# print(test)

# user = User.query.filter_by(username='admin').first()
# 实现model 里面orm 数据操作
# app = Flask(__name__)
# app.config.from_object('conf.Config')
# db.init_app(app=app)
# 没有上下文,需要重新 push 一下
# app.app_context().push()
# user = User.query.all()
# print(type(user))
# db.create_all()
# db.drop_all()
# print(user[0].username)

# user = User.query.filter_by(username='adminadmin').first()
# print(user)

# question = Question.query.get(5)
# print(question)
# answer = question.answer_list.filter_by(is_valid=True).first()
# print(answer)