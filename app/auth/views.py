from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from app.auth import auth_bp

USER_DATA = {
    "username": "user1",
    "password": "123"
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == USER_DATA['username'] and password == USER_DATA['password']:
            session['user'] = username
            flash('Успішний вхід до системи!', 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Wrong data! Try again!', 'danger')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html', title="Login")

@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        flash('Будь ласка, увійдіть у систему.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            key = request.form.get('cookie_key')
            value = request.form.get('cookie_value')
            max_age = request.form.get('cookie_max_age', type=int)
            
            if key and value:
                resp = make_response(redirect(url_for('auth.profile')))
                resp.set_cookie(key, value, max_age=max_age if max_age else None)
                flash(f'Кукі "{key}" успішно додано!', 'success')
                return resp
            else:
                flash('Введіть ключ та значення кукі!', 'danger')
                
        elif action == 'delete_one':
            key = request.form.get('delete_key')
            if key in request.cookies:
                resp = make_response(redirect(url_for('auth.profile')))
                resp.set_cookie(key, '', expires=0)
                flash(f'Кукі "{key}" видалено!', 'info')
                return resp
            else:
                flash(f'Кукі з ключем "{key}" не знайдено.', 'warning')
                
        elif action == 'delete_all':
            resp = make_response(redirect(url_for('auth.profile')))
            for cookie_key in request.cookies:
                if cookie_key != 'session':
                    resp.set_cookie(cookie_key, '', expires=0)
            flash('Всі кукі успішно видалено!', 'info')
            return resp

    current_cookies = request.cookies
    username = session.get('user')
    theme = request.cookies.get('theme', 'light')

    return render_template('auth/profile.html', title="Profile", username=username, cookies=current_cookies, theme=theme)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/set-theme/<theme_name>')
def set_theme(theme_name):
    resp = make_response(redirect(url_for('auth.profile')))
    if theme_name in ['light', 'dark']:
        resp.set_cookie('theme', theme_name, max_age=60*60*24*30)
        flash(f'Змінено кольорову схему на {theme_name}', 'success')
    return resp