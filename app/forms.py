from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message="Ім'я є обов'язковим"), 
        Length(min=4, max=10, message="Довжина імені має бути від 4 до 10 символів")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message="Email є обов'язковим"), 
        Email(message="Некоректний формат email")
    ])
    
    phone = StringField('Phone', validators=[
        DataRequired(message="Телефон є обов'язковим"),
        Regexp(r'^\+380\d{9}$', message="Формат телефону має бути: +380XXXXXXXXX")
    ])
    
    subject = SelectField('Subject', choices=[
        ('support', 'Технічна підтримка'),
        ('sales', 'Відділ продажів'),
        ('cooperation', 'Співпраця')
    ], validators=[DataRequired()])
    
    message = TextAreaField('Message', validators=[
        DataRequired(message="Повідомлення є обов'язковим"),
        Length(max=500, message="Повідомлення не повинно перевищувати 500 символів")
    ])
    
    submit = SubmitField('Send Message')