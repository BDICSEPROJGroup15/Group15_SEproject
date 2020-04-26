from flask import Blueprint

blog=Blueprint('blog',__name__,url_prefix='/blog',static_url_path='/blog/static',static_folder='static')

@blog.route("/")
@blog.route("/index")
def index():
    return "blog"