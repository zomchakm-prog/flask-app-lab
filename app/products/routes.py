import os
import uuid
from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename
from app.products import products_bp
from app.products.forms import ProductForm
from app.products.models import ProductModel

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

 
@products_bp.route('/')
def index():
    all_products = ProductModel.get_all()  
    return render_template('products/index.html', products=all_products, title="Каталог товарів")

 
@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_filename = None
        
        f = form.image.data
        if f:
            filename = secure_filename(f.filename)
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            image_filename = f"{uuid.uuid4().hex}.{ext}"
            
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            f.save(os.path.join(upload_folder, image_filename))
            
        ProductModel.create(form, image_filename)
        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.index'))
        
    return render_template('products/add.html', form=form, title="Додати товар")

 
@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = ProductModel.get_by_id(product_id)
    if not product:
        flash('Товар не знайдено!', 'danger')
        return redirect(url_for('products.index'))
    return render_template('products/detail.html', product=product, title=product['name'])

 
@products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = ProductModel.get_by_id(product_id)
    if not product:
        flash('Товар не знайдено!', 'danger')
        return redirect(url_for('products.index'))
        
    form = ProductForm(data=product)
    if form.validate_on_submit():
        image_filename = product.get('image')
        
        f = form.image.data
        if f and f.filename:
            filename = secure_filename(f.filename)
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
            image_filename = f"{uuid.uuid4().hex}.{ext}"
            
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            f.save(os.path.join(upload_folder, image_filename))
            
        ProductModel.update(product_id, form, image_filename)
        flash('Товар успішно оновлено!', 'success')
        return redirect(url_for('products.product_detail', product_id=product_id))
        
    return render_template('products/edit.html', form=form, product=product, title="Редагувати товар")

 
@products_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product = ProductModel.get_by_id(product_id)
    if product:
        ProductModel.delete(product_id)
        flash('Товар успішно видалено!', 'success')
    else:
        flash('Товар не знайдено!', 'danger')
    return redirect(url_for('products.index'))