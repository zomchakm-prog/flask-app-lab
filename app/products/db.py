import os
from tinydb import TinyDB


os.makedirs('data', exist_ok=True)


db = TinyDB('data/products.json')
products_table = db.table('products')