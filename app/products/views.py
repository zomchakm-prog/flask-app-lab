import os
import uuid
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, abort, current_app
from tinydb import Query
from app.products import products_bp
from .db import products_table
from .forms import ProductForm

@products_bp.route('/')
def product_list():
    all_products = products_table.all()
    return render_template('products/products.html', products=all_products)

@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    product_q = Query()
    product = products_table.get(product_q.id == product_id)
    if not product:
        abort(404)
    return render_template('products/detail_product.html', product=product)

@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_path = ""
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            file = form.image.data
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            
             
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            image_path = f"uploads/{filename}"

        all_items = products_table.all()
        new_id = max([item.get('id', 0) for item in all_items], default=0) + 1

        new_product = {
            'id': new_id,
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        products_table.insert(new_product)
        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.product_list'))

    return render_template('products/add_product.html', form=form)

@products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product_q = Query()
    product = products_table.get(product_q.id == product_id)
    if not product:
        flash('Товар не знайдено.', 'danger')
        return redirect(url_for('products.product_list'))

    form = ProductForm(data=product)
    if form.validate_on_submit():
        image_path = product.get('image', '')
        
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            file = form.image.data
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            image_path = f"uploads/{filename}"

        products_table.update({
            'name': form.name.data,
            'content': form.content.data,
            'price': float(form.price.data),
            'category': form.category.data,
            'quantity': form.quantity.data,
            'image': image_path
        }, product_q.id == product_id)

        flash('Товар успішно оновлено!', 'success')
        return redirect(url_for('products.product_detail', product_id=product_id))

    return render_template('products/edit_product.html', form=form, product=product)

@products_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    product_q = Query()
    if products_table.contains(product_q.id == product_id):
        products_table.remove(product_q.id == product_id)
        flash('Товар успішно видалено!', 'success')
    else:
        flash('Товар не знайдено.', 'danger')
    return redirect(url_for('products.product_list'))