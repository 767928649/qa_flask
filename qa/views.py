# -*- coding: utf-8 -*-
# @Time    : 2022/5/19 下午4:35
# @Author  : Ly
from flask_login import login_required, current_user
from qa.forms import WriterQuestionForm, WriteAnswerForm
from models import Question, Answer, AnswerComment, db
from flask import Blueprint, render_template, request, abort, flash, redirect, url_for, app, jsonify

# 引用蓝图
qa = Blueprint('qa', __name__,
               template_folder='templates',
               static_folder='../assets')


@qa.route('/')
def index():
    """
    回答列表
    :return:
    """
    per_page = 5  # 每页数据的大小
    print(request.path)
    page = int(request.args.get('page', 1))
    print(page)
    page_data = Answer.query.filter_by(is_valid=True).paginate(
        page=page, per_page=per_page)
    posts = page_data.items
    print(posts)
    return render_template('index.html', page_data=page_data)


@qa.route('/follow')
def follow():
    # 关注页
    """ 关注 问题列表 """
    per_page = 20  # 每页数据的大小
    page = int(request.args.get('page', 1))
    page_data = Question.query.filter_by(is_valid=True).paginate(
        page=page, per_page=per_page)
    return render_template('follow.html', page_data=page_data)


@qa.route('/qa/list')
def question_list():
    """
    查询问题数据列表
    // json
    {
        'code':0
    }
    """
    try:
        per_page = 2  # 每页数据的大小
        page = int(request.args.get('page', 1))
        page_data = Question.query.filter_by(is_valid=True).paginate(
            page=page, per_page=per_page)
        data = render_template('question_list.html', page_data=page_data)
        return {'code': 0, 'data': data}
    except Exception as e:
        print(e)
    return {'code': 1, 'data': ''}


@qa.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    # 写文章
    form = WriterQuestionForm()
    if form.validate_on_submit():
        try:
            que_obj = form.save()
            flash('发布成功', 'success')
            return redirect(url_for('qa.index'))
        except Exception as e:
            print(e)
            flash('发布失败,请稍后再试!', 'danger')
    return render_template('write.html', form=form)


@qa.route('/detail/<int:q_id>', methods=['GET', 'POST'])
def detail(q_id):
    # 问题详情页
    # 查询问题信息
    question = Question.query.get(q_id)
    # print(question)
    if not question.is_valid:
        abort(404)
    # 展示第一条回答信息
    answer = question.answer_list.filter_by(is_valid=True).first()
    print(answer)
    print(question.id)
    # 添加回答
    form = WriteAnswerForm()
    if form.validate_on_submit():
        try:
            if not current_user.is_authenticated:
                # next_url = request.path
                # print(next_url)
                flash('请先登录!', 'danger')
                return redirect(url_for('accounts.login'))
            form.save(question=question)
            flash('回答问题成功', 'success')
            return redirect(url_for('qa.detail', q_id=q_id))
        except Exception as e:
            print(e)
    return render_template('detail.html', question=question, answer=answer, form=form)


@qa.route('/comments/<int:answer_id>', methods=['GET', 'POST'])
def comments(answer_id):
    """ 评论 """
    answer = Answer.query.get(answer_id)
    if request.method == 'POST':
        # 添加评论
        try:
            if not current_user.is_authenticated:
                result = {'code': 1, 'message': '请登录'}
                return jsonify(result), 400
            # 1. 获取数据
            content = request.form.get('content', '')
            reply_id = request.form.get('reply_id', None)
            # 2. 保存到数据库
            question = answer.question
            comment_obj = AnswerComment(content=content,
                                        user=current_user,
                                        answer=answer,
                                        reply_id=reply_id,
                                        question=question
                                        )
            db.session.add(comment_obj)
            db.session.commit()
            return '', 201
        except Exception as e:
            result = {'code': 1, 'message': '服务器正忙，请稍后重试'}
            return jsonify(result), 400
    else:
        # 获取评论列表
        try:
            page = int(request.args.get('page', 1))
            page_data = answer.comment_list().paginate(page=page, per_page=1)
            data = render_template('comments.html', page_data=page_data, answer=answer)
            return jsonify({'code': 0, 'data': data, 'meta': {'page': page}}), 200
        except Exception as e:
            print(e)
            return jsonify({'code': 1, 'data': '', 'message': '服务器正忙'}), 500


@qa.route('/comment/love/<int:comment_id>', methods=['POST'])
def comment_love(comment_id):
    """评论点赞"""
    print(request.path)
    print(comment_id)
    try:
        if not current_user.is_authenticated:
            return jsonify({'code': 0, 'message': '请登录'}), 401
        comment_obj = AnswerComment.query.get(comment_id)
        comment_obj.love_count += 1
        db.session.add(comment_obj)
        db.session.commit()
        return jsonify({'code': 0, 'message': 'success'}), 201
    except Exception as e:
        print(e)
        return jsonify({'code': 1, 'data': '', 'message': '服务器正忙'}), 500


@qa.route('/ajax/jq')
def test():
    return render_template('ajax_shortcut.html')


@qa.route('/ajax/js', methods=['GET', 'POST'])
def ajax_js():
    import json
    print(request.values)
    user = {
        'username': '张三',
        'nickname': '昵称',
        'profile': {
            'age': 23
        }
    }
    return json.dumps(user), 401