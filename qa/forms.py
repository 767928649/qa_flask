# -*- coding: utf-8 -*-
# @Time    : 2022/5/21 下午7:25
# @Author  : Ly
import os
from flask_ckeditor import CKEditorField
from flask import current_app
from flask_wtf import FlaskForm
from flask_login import current_user
from werkzeug.utils import secure_filename
from models import Question, db, QuestionTags, Answer
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length


class WriterQuestionForm(FlaskForm):
    """
    写文章
    """
    img = FileField(label='上传图片', render_kw={
        'accept': ".jpeg, .jpg, .png"
    })
    title = StringField(label='标题', render_kw={
        'class': "form-control",
        'placeholder': "请输入标题（最多50个字"
    }, validators=[DataRequired('请输入标题'),
                   Length(min=3, max=50, message='标题长度为 5-50 个字符')])

    tags = StringField(label='标签', render_kw={
        'class': "form-control",
        'placeholder': "请用逗号隔开"
    })
    desc = TextAreaField(label='描述', render_kw={
        'class': "form-control",
        'placeholder': "描述"
    }, validators=[Length(max=150, message='描述最长150个字符')])
    content = CKEditorField(label='正文', render_kw={
        'class': "form-control",
        'placeholder': "正文"
    }, validators=[Length(min=10, message='正文不能低于10个字符')])

    def save(self):
        """
        发布问题
        :return:
        """
        # 1.和获取图片
        img = self.img.data
        print(img)
        if img:
            img_name = secure_filename(img.filename)
            print(current_app)  # 通过注册的 app 应用获取加载进去的 app 配置文件获取配置拿到图片保存的地址
            img_path = os.path.join(current_app.config['MEDIA_ROOT'], img_name)
            img.save(img_path)
        # 2.保存问题
        title = self.title.data
        desc = self.desc.data
        content = self.content.data
        print(current_user)  # 通过 current_user 获取 user 对象
        que_obj = Question(img=img_name, title=title, desc=desc, content=content, user=current_user)
        db.session.add(que_obj)
        # 保存标签
        tags = self.tags.data
        for tag_name in tags.split(','):
            if tag_name:
                tag_obj = QuestionTags(tag_name=tag_name, question=que_obj)
                db.session.add(tag_obj)
            db.session.commit()
        return que_obj


class WriteAnswerForm(FlaskForm):
    """
    写回答
    """
    content = CKEditorField(label='回答内容', validators=[DataRequired('内容不能为空'),
                                                      Length(min=5, message='回答内容至少 5 个字符')])

    def save(self, question):
        """
        保存表单数据
        :return:
        """
        content = self.content.data
        print(content)
        print(question)
        print(current_user)
        user = current_user
        answer_obj = Answer(content=content, user=user, question=question)
        # print(answer_obj)
        db.session.add(answer_obj)
        db.session.commit()
        return answer_obj