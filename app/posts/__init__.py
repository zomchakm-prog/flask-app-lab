from flask import Blueprint

post_bp = Blueprint('posts', __name__, template_folder='templates', static_folder='static')

from app.posts import views