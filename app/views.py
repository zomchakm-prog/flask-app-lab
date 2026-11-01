import logging
from flask import render_template, request, redirect, url_for, flash
from app import app
from app.forms import ContactForm

 
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def resume():
    return render_template('resume.html', title="Резюме - Максим Зомчак")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти - Максим Зомчак")

@app.route('/homepage')
def home():
    agent = request.user_agent
    return render_template('homepage.html', title="Головна сторінка", agent=agent)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data
        
        
        logging.info(f"Contact form submitted: Name={name}, Email={email}, Phone={phone}, Subject={subject}")
        
        flash('Повідомлення успішно відправлено та збережено!', 'success')
        return redirect(url_for('contact'))  
        
    if form.errors and request.method == 'POST':
        flash('Помилка при заповненні форми. Перевірте введені дані.', 'danger')
        
    return render_template('contact.html', form=form)