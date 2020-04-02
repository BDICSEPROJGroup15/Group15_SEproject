from flask_script import Manager, Server
from src import app

# 自定义的控制台
# 控制台 输入 python script.py shell 可以打开自定义的控制台，类似于flask shell
# 输入 python script.py xxx 可以使用自定义命令，比如server是启动服务器

manager = Manager(app)

# 自定义命令 xxx
manager.add_command("server",Server())

@manager.shell
# 用shell 命令创建命令行
def make_shell_context():
    return dict(app=app)

if __name__=="__main__":
    manager.run()