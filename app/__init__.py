from flask import Flask

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'   

 
from app.users import users_bp
from app.products import products_bp
from app.auth import auth_bp   

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(products_bp, url_prefix='/products')
app.register_blueprint(auth_bp)        

from app import views