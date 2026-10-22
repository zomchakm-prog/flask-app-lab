from flask import render_template, request
from app import app

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