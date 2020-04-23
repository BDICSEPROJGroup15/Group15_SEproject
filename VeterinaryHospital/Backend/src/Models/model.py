from src import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


# 应用修改自 TodoMVC 的 todo list 应用，使用 Mariadb 作为数据库后端，Bootstrap 作为前端的 Flask 应用。先给它起个好听的名字吧，方便之后称呼。
#
# todo list => (自定义，随便起名称)  => todoest
#
#
# 就像一般的 todo list 应用一样，todoest 实现了以下功能：
# - 管理数据库连接
# - 列出所有的 todo 项
# - 创建新的 todo
# - 检索单个 todo
# - 编辑单个 todo 或将其标记为已完成
# - 删除单个 todo

class User1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),unique=True)
    password_hash= db.Column(db.String(50),unique=True)
    email = db.Column(db.String(50),unique=True)
    # 添加一列数据，更新数据库又不能删除原来的表，只能通过magrate模块来调整
    # gender=db.Column(db.SmallInteger,default=1)
    # 创建账户时间，默认utc时间，在显示页面moment方法进行转化
    # 使用协调时间时（Coordinated Universal Time,UTC）协调世界各地的时差问题;
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    todos = db.relationship('Todo', backref='user')

    categorys = db.relationship('Category',backref='user')

    # 密码查看保护
    @property
    def password(self):
        """u.password"""
        raise ArithmeticError('Password is not accessible')

    @password.setter
    def password(self,password):
        """将密码进行hash加密"""
        self.password_hash=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<User %s>'%self.username

    #任务和类的关系，一对多
    #分类一，任务是多，外键写在一端
class Todo(db.Model):
    id = db.Column(db.Integer,autoincrement = True, primary_key=True )
    content = db.Column(db.String(50),unique=True)
    # 任务状态，一般刚创建默认未完成
    status = db.Column(db.Boolean, default=False)
    add_time=db.Column(db.DateTime,default=datetime.utcnow())
    # 和用户表关联
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'))

    def __repr__(self):
        return '<TODO %s>'%self.content[:5]

class Category(db.Model):
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String(50),unique=True)
    add_time=db.Column(db.DateTime,default=datetime.utcnow())
    #关联任务表
    todos = db.relationship('Todo',backref='category')
    #关联用户表
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Category>"%(self.name)
