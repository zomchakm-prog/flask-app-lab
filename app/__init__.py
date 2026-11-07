from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import DevelopmentConfig

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

 
from app.posts.models import Post

from app.users import users_bp
from app.products import products_bp

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')

from app import views

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

 
from app.posts import post_bp
app.register_blueprint(post_bp, url_prefix='/posts')