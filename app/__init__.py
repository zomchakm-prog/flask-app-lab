from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-zomchak'  

from app.users import users_bp
from app.products import products_bp

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')

from app import views