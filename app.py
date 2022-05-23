from models import db, User
from qa.views import qa
from flask_login import LoginManager
from flask import Flask
from flask_ckeditor import CKEditor
from accounts.views import accounts
from utils.filters import number_split
from utils.validators import dt_format_show

app = Flask(__name__, static_folder='medias')
# 从配置文件加载配置
app.config.from_object('conf.Config')

# 初始化数据库
db.init_app(app)

# 初始化富文本 ckeditor
CKEditor = CKEditor()
CKEditor.init_app(app)

# 登录验证的初始化
login_manager = LoginManager()
login_manager.login_view = "accounts.login"
login_manager.login_message = '请登录'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)

# 注册蓝图
app.register_blueprint(accounts, url_prefix='/accounts')
app.register_blueprint(qa, url_prefix='/')

# 注册自定义过滤器
app.jinja_env.filters['number_split'] = number_split
app.jinja_env.filters['dt_format_show'] = dt_format_show


# @app.before_request
# def before_request():
#     """
#     如果有用户 id,设置到全局对象
#     :return:
#     """
#     # 从 session 中取,因为在视图def login():里面把 user_id 加入到了 session
#     user_id = session.get('user_id', None)
#     if user_id:
#         user = User.query.get(user_id)
#         print(user)
#         g.current_user = user

# 返回视图中login_user(user)的回调
# 接受登录用户的 id 号,并返回 user 用户模型,因为他需要被 flask_login 所调用,所以我们要在这里打上@login_manager.user_loader,
# 当没有sessionID时，通过装饰器指定的函数来读取用户到session中，达到在前端模板中调用当前登录用户current_user的目的，该装饰器就是：
# 他的作用就是即使你的user参数无值，也可以通过调用self.callback来得到这个user，并把这个user赋值给ctx.user
# 回调函数,login_user 执行时候,回调load_user把 user id 载入到 session 中
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


app.run()